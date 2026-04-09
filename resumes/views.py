"""
Views for Resume Generator
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
import os
import io
import sys
from pathlib import Path

from .models import (
    CustomUser, UserProfile, UserResumeData, UserDirectory,
    Resume, ResumeTemplate, ColorScheme, UserColorScheme, ResumeGenerationJob
)
from .serializers import (
    UserResumeDataSerializer, ResumeSerializer, ColorSchemeSerializer,
    UserColorSchemeSerializer, ResumeGenerationJobSerializer
)

User = get_user_model()

LENGTH_VARIANTS = {
    "long": "Long (Full Detail)",
    "short": "Short (3-4 Pages)",
    "brief": "Brief (1-2 Pages)",
}

COLOR_SCHEMES = [
    "default_professional", "corporate_blue", "modern_tech", "modern_clean",
    "satellite_imagery", "terrain_mapping", "cartographic_professional", "topographic_classic",
]

FORMAT_CONTENT_TYPES = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "rtf": "application/rtf",
    "md": "text/markdown",
}


def download_form(request):
    """Public form page for downloading resumes — no login required.

    Populates archetype dropdown from database. Archetype metadata
    (names, slugs, descriptions) is embedded as JSON for JS dropdown
    descriptions.
    """
    from portfolio.services import get_archetype_metadata
    from portfolio.models import PersonalInfo as PortfolioPersonalInfo
    import json as json_module

    archetypes = get_archetype_metadata()

    # Load personal info for hero, footer, links
    try:
        info = PortfolioPersonalInfo.objects.prefetch_related("social_links").get()
    except PortfolioPersonalInfo.DoesNotExist:
        info = None

    context = {
        "info": info,
        "social_links": info.social_links.all() if info else [],
        "archetypes": archetypes,
        "archetype_json": json_module.dumps(archetypes),
        "length_variants": LENGTH_VARIANTS.items(),
        "color_schemes": [(s, s.replace("_", " ").title()) for s in COLOR_SCHEMES],
        "formats": [("pdf", "PDF"), ("docx", "Word (DOCX)"), ("rtf", "RTF"), ("md", "Markdown")],
    }
    return render(request, "resumes/download_form.html", context)


@require_http_methods(["POST"])
def generate_on_demand(request):
    """Generate a resume on-demand and stream it as a download — no login required.

    Reads from database via portfolio.services, applies length truncation,
    generates the requested format in memory, and returns it.
    """
    archetype_slug = request.POST.get("resume_type", "comprehensive")
    length_variant = request.POST.get("length_variant", "long")
    color_scheme = request.POST.get("color_scheme", "default_professional")
    format_type = request.POST.get("format_type", "pdf")
    output_type = request.POST.get("output_type", "ats")

    # Validate
    if length_variant not in LENGTH_VARIANTS:
        return HttpResponse("Invalid length variant", status=400)
    if color_scheme not in COLOR_SCHEMES:
        return HttpResponse("Invalid color scheme", status=400)
    if format_type not in FORMAT_CONTENT_TYPES:
        return HttpResponse("Invalid format", status=400)

    # Build resume data from database
    from portfolio.services import build_resume_data_from_db
    from portfolio.models import ResumeArchetype

    try:
        ResumeArchetype.objects.get(slug=archetype_slug)
    except ResumeArchetype.DoesNotExist:
        return HttpResponse("Invalid resume type", status=400)

    resume_data = build_resume_data_from_db(archetype_slug, output_type)

    # Apply length truncation
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from master_resume_generator import create_abbreviated_resume, create_brief_resume

    if length_variant == "short":
        resume_data = create_abbreviated_resume(resume_data, archetype_slug)
    elif length_variant == "brief":
        resume_data = create_brief_resume(resume_data, archetype_slug)

    # Load color scheme config
    from .core_services import ResumeGenerator
    color_config_path = project_root / "color_schemes" / f"{color_scheme}.json"
    config = {}
    if color_config_path.exists():
        with open(color_config_path, "r") as f:
            config = json.load(f)

    # Create generator from data
    generator = ResumeGenerator.from_data(
        resume_data=resume_data,
        config=config,
        color_scheme=color_scheme,
        length_variant=length_variant,
        output_type=output_type,
    )

    # Generate to memory buffer
    filename = f"dheeraj_chand_{archetype_slug}_{length_variant}_{color_scheme}.{format_type}"
    buffer = io.BytesIO()

    if format_type == "pdf":
        generator.generate_pdf(buffer)
        buffer.seek(0)
    elif format_type == "docx":
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=True) as tmp:
            generator.generate_docx(tmp.name)
            with open(tmp.name, "rb") as f:
                buffer.write(f.read())
            buffer.seek(0)
    elif format_type == "rtf":
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".rtf", delete=True, mode="w") as tmp:
            generator.generate_rtf(tmp.name)
            with open(tmp.name, "rb") as f:
                buffer.write(f.read())
            buffer.seek(0)
    elif format_type == "md":
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".md", delete=True, mode="w") as tmp:
            generator.generate_markdown(tmp.name)
            with open(tmp.name, "rb") as f:
                buffer.write(f.read())
            buffer.seek(0)

    content_type = FORMAT_CONTENT_TYPES[format_type]
    response = HttpResponse(buffer.read(), content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@login_required
def dashboard(request):
    """User dashboard view"""
    user = request.user
    
    # Get user's resume data
    resume_data = UserResumeData.objects.filter(user=user, is_active=True)
    
    # Get user's generated resumes
    resumes = Resume.objects.filter(user=user)
    
    # Get recent generation jobs
    recent_jobs = ResumeGenerationJob.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get available color schemes
    color_schemes = ColorScheme.objects.filter(is_active=True)
    
    # Get available templates
    templates = ResumeTemplate.objects.filter(is_active=True)
    
    context = {
        'user': user,
        'resume_data': resume_data,
        'resumes': resumes,
        'recent_jobs': recent_jobs,
        'color_schemes': color_schemes,
        'templates': templates,
        'resume_types': [
            ('comprehensive', 'Comprehensive'),
            ('polling_research_redistricting', 'Polling/Research/Redistricting'),
            ('marketing', 'Marketing'),
            ('data_analysis', 'Data Analysis'),
            ('visualisation', 'Visualization'),
            ('product', 'Product'),
        ],
        'length_variants': [
            ('long', 'Long (3+ pages)'),
            ('short', 'Short (1-2 pages)'),
        ]
    }
    
    return render(request, 'resumes/dashboard.html', context)


@login_required
def resume_detail(request, resume_id):
    """Resume detail view"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    context = {
        'resume': resume,
        'file_paths': resume.get_file_paths() if hasattr(resume, 'get_file_paths') else [],
    }
    
    return render(request, 'resumes/resume_detail.html', context)


@login_required
@require_http_methods(["POST"])
def generate_resume(request):
    """Generate resume for user"""
    try:
        data = json.loads(request.body)
        resume_type = data.get('resume_type')
        length_variant = data.get('length_variant')
        color_scheme = data.get('color_scheme', 'default_professional')
        formats = data.get('formats', ['pdf', 'docx'])
        
        # Get or create user resume data
        resume_data, created = UserResumeData.objects.get_or_create(
            user=request.user,
            resume_type=resume_type,
            length_variant=length_variant,
            defaults={'is_active': True}
        )
        
        # Create generation job
        job = ResumeGenerationJob.objects.create(
            user=request.user,
            resume=resume_data,
            job_id=f"job_{request.user.id}_{resume_type}_{length_variant}",
            formats=formats,
            color_scheme=ColorScheme.objects.get(name=color_scheme) if color_scheme else None,
            status='queued'
        )
        
        # TODO: Start background task for resume generation
        # For now, just return success
        
        return JsonResponse({
            'success': True,
            'job_id': job.job_id,
            'message': 'Resume generation started'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
def download_resume(request, resume_id, format_type):
    """Download generated resume file"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Get file path based on format
    file_path = None
    if format_type == 'pdf':
        file_path = resume.pdf_path
    elif format_type == 'docx':
        file_path = resume.docx_path
    elif format_type == 'rtf':
        file_path = resume.rtf_path
    
    if not file_path or not os.path.exists(file_path):
        return HttpResponse('File not found', status=404)
    
    # Return file for download
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.{format_type}"'
        return response


class UserResumeDataViewSet(viewsets.ModelViewSet):
    """API viewset for user resume data"""
    serializer_class = UserResumeDataSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserResumeData.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """Generate resume from user data"""
        resume_data = self.get_object()
        
        # Create generation job
        job = ResumeGenerationJob.objects.create(
            user=request.user,
            resume=resume_data,
            job_id=f"api_job_{request.user.id}_{resume_data.resume_type}_{resume_data.length_variant}",
            formats=request.data.get('formats', ['pdf']),
            status='queued'
        )
        
        # TODO: Start background task
        
        return Response({
            'job_id': job.job_id,
            'status': 'queued'
        })


class ResumeViewSet(viewsets.ModelViewSet):
    """API viewset for resumes"""
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """Get generated files for resume"""
        resume = self.get_object()
        file_paths = resume.get_file_paths() if hasattr(resume, 'get_file_paths') else []
        return Response({'files': file_paths})


class ColorSchemeViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for color schemes"""
    serializer_class = ColorSchemeSerializer
    queryset = ColorScheme.objects.filter(is_active=True)


class UserColorSchemeViewSet(viewsets.ModelViewSet):
    """API viewset for user custom color schemes"""
    serializer_class = UserColorSchemeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only the current user's color schemes"""
        return UserColorScheme.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically assign the current user when creating"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a color scheme"""
        original = self.get_object()
        
        # Create a copy with a new name
        copy_data = {
            'name': f"{original.name} (Copy)",
            'slug': f"{original.slug}-copy",
            'description': original.description,
            'primary_color': original.primary_color,
            'secondary_color': original.secondary_color,
            'accent_color': original.accent_color,
            'muted_color': original.muted_color,
            'background_color': original.background_color,
            'text_color': original.text_color,
        }
        
        serializer = self.get_serializer(data=copy_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResumeGenerationJobViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for generation jobs"""
    serializer_class = ResumeGenerationJobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ResumeGenerationJob.objects.filter(user=self.request.user)