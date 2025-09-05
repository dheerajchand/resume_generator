"""
Django views for Resume Generator
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import uuid
import os
from datetime import datetime

from .models import (
    Resume, ResumeTemplate, PersonalInfo, Experience, Project, 
    Education, Certification, Achievement, Competency, CompetencyCategory,
    ColorScheme, ResumeGenerationJob
)
from .serializers import ResumeSerializer, PersonalInfoSerializer
from .services import ResumeGenerationService, ContentManagementService


def home(request):
    """Home page view"""
    return render(request, 'resumes/home.html')


class ResumeListView(LoginRequiredMixin, ListView):
    """List all resumes for the current user"""
    model = Resume
    template_name = 'resumes/resume_list.html'
    context_object_name = 'resumes'
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a specific resume"""
    model = Resume
    template_name = 'resumes/resume_detail.html'
    context_object_name = 'resume'
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """Create a new resume"""
    model = Resume
    template_name = 'resumes/resume_form.html'
    fields = ['title', 'description', 'template']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('resume_detail', kwargs={'pk': self.object.pk})


class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing resume"""
    model = Resume
    template_name = 'resumes/resume_form.html'
    fields = ['title', 'description', 'template']
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a resume"""
    model = Resume
    template_name = 'resumes/resume_confirm_delete.html'
    success_url = reverse_lazy('resume_list')
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


@login_required
def dashboard(request):
    """Main dashboard view"""
    user = request.user
    
    # Get user's data counts
    context = {
        'resume_count': Resume.objects.filter(user=user).count(),
        'experience_count': Experience.objects.filter(user=user).count(),
        'project_count': Project.objects.filter(user=user).count(),
        'recent_resumes': Resume.objects.filter(user=user).order_by('-created_at')[:5],
        'templates': ResumeTemplate.objects.filter(is_active=True),
        'color_schemes': ColorScheme.objects.filter(is_active=True),
    }
    
    return render(request, 'resumes/dashboard.html', context)


@login_required
def generate_resume(request, resume_id):
    """Generate resume files"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Get generation parameters
            formats = request.POST.getlist('formats', ['pdf'])
            color_scheme_id = request.POST.get('color_scheme')
            
            # Create generation job
            job = ResumeGenerationJob.objects.create(
                user=request.user,
                resume=resume,
                job_id=str(uuid.uuid4()),
                formats=formats,
                color_scheme_id=color_scheme_id if color_scheme_id else None,
                status='queued'
            )
            
            # Start generation (async in production)
            generation_service = ResumeGenerationService()
            result = generation_service.generate_resume(resume, formats, color_scheme_id)
            
            if result['success']:
                job.status = 'completed'
                job.result_files = result['files']
                job.completed_at = datetime.now()
                job.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Resume generated successfully',
                    'files': result['files']
                })
            else:
                job.status = 'failed'
                job.error_message = result['error']
                job.save()
                
                return JsonResponse({
                    'success': False,
                    'message': result['error']
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error generating resume: {str(e)}'
            })
    
    return render(request, 'resumes/generate_resume.html', {'resume': resume})


@login_required
def download_resume(request, resume_id, format_type):
    """Download generated resume file"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    file_path = None
    if format_type == 'pdf' and resume.pdf_path:
        file_path = resume.pdf_path
    elif format_type == 'docx' and resume.docx_path:
        file_path = resume.docx_path
    elif format_type == 'rtf' and resume.rtf_path:
        file_path = resume.rtf_path
    
    if not file_path or not os.path.exists(file_path):
        return JsonResponse({'error': 'File not found'}, status=404)
    
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.{format_type}"'
        return response


# API Views
class ResumeAPIView:
    """API view for resume operations"""
    
    @staticmethod
    def get_resume_data(request, resume_id):
        """Get resume data as JSON"""
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        serializer = ResumeSerializer(resume)
        return JsonResponse(serializer.data)
    
    @staticmethod
    def update_resume_data(request, resume_id):
        """Update resume data from JSON"""
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        
        try:
            data = json.loads(request.body)
            resume.content = data
            resume.save()
            
            return JsonResponse({'success': True, 'message': 'Resume updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    @staticmethod
    def get_personal_info(request):
        """Get user's personal information"""
        try:
            personal_info = PersonalInfo.objects.get(user=request.user)
            serializer = PersonalInfoSerializer(personal_info)
            return JsonResponse(serializer.data)
        except PersonalInfo.DoesNotExist:
            return JsonResponse({'error': 'Personal information not found'}, status=404)
    
    @staticmethod
    def update_personal_info(request):
        """Update user's personal information"""
        try:
            personal_info, created = PersonalInfo.objects.get_or_create(user=request.user)
            data = json.loads(request.body)
            
            for field, value in data.items():
                if hasattr(personal_info, field):
                    setattr(personal_info, field, value)
            
            personal_info.save()
            return JsonResponse({'success': True, 'message': 'Personal information updated'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def preview_resume(request, resume_id):
    """Preview resume in browser"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Generate preview content
    content_service = ContentManagementService()
    preview_data = content_service.generate_preview_content(resume)
    
    return render(request, 'resumes/resume_preview.html', {
        'resume': resume,
        'preview_data': preview_data
    })


@login_required
def template_gallery(request):
    """Show available resume templates"""
    templates = ResumeTemplate.objects.filter(is_active=True)
    color_schemes = ColorScheme.objects.filter(is_active=True)
    
    return render(request, 'resumes/template_gallery.html', {
        'templates': templates,
        'color_schemes': color_schemes
    })


@login_required
def content_editor(request, resume_id):
    """Content editor for resume"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Get all user's data for editing
    context = {
        'resume': resume,
        'personal_info': PersonalInfo.objects.filter(user=request.user).first(),
        'experiences': Experience.objects.filter(user=request.user).order_by('-start_date'),
        'projects': Project.objects.filter(user=request.user).order_by('-start_date'),
        'educations': Education.objects.filter(user=request.user).order_by('-start_date'),
        'certifications': Certification.objects.filter(user=request.user).order_by('-issue_date'),
        'achievements': Achievement.objects.filter(user=request.user).order_by('-date'),
        'competency_categories': CompetencyCategory.objects.all().prefetch_related('competencies'),
    }
    
    return render(request, 'resumes/content_editor.html', context)


# AJAX endpoints
@login_required
def add_experience(request):
    """Add new experience entry"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            experience = Experience.objects.create(user=request.user, **data)
            return JsonResponse({
                'success': True,
                'id': experience.id,
                'message': 'Experience added successfully'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def add_project(request):
    """Add new project entry"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project = Project.objects.create(user=request.user, **data)
            return JsonResponse({
                'success': True,
                'id': project.id,
                'message': 'Project added successfully'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def update_competencies(request):
    """Update user competencies"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            competency_ids = data.get('competency_ids', [])
            
            # Clear existing competencies for user
            Competency.objects.filter(user=request.user).delete()
            
            # Add selected competencies
            for comp_id in competency_ids:
                competency = Competency.objects.get(id=comp_id)
                competency.user = request.user
                competency.save()
            
            return JsonResponse({'success': True, 'message': 'Competencies updated'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)