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
from pathlib import Path

from .models import (
    CustomUser, UserProfile, UserResumeData, UserDirectory,
    Resume, ResumeTemplate, ColorScheme, ResumeGenerationJob
)
from .serializers import (
    UserResumeDataSerializer, ResumeSerializer, ColorSchemeSerializer,
    ResumeGenerationJobSerializer
)

User = get_user_model()


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


class ResumeGenerationJobViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for generation jobs"""
    serializer_class = ResumeGenerationJobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ResumeGenerationJob.objects.filter(user=self.request.user)