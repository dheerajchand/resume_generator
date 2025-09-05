"""
URL configuration for resumes app
"""

from django.urls import path, include
from . import views

app_name = 'resumes'

urlpatterns = [
    # Main views
    path('', views.dashboard, name='dashboard'),
    path('resumes/', views.ResumeListView.as_view(), name='resume_list'),
    path('resumes/<int:pk>/', views.ResumeDetailView.as_view(), name='resume_detail'),
    path('resumes/create/', views.ResumeCreateView.as_view(), name='resume_create'),
    path('resumes/<int:pk>/edit/', views.ResumeUpdateView.as_view(), name='resume_edit'),
    path('resumes/<int:pk>/delete/', views.ResumeDeleteView.as_view(), name='resume_delete'),
    
    # Resume operations
    path('resumes/<int:resume_id>/generate/', views.generate_resume, name='generate_resume'),
    path('resumes/<int:resume_id>/preview/', views.preview_resume, name='preview_resume'),
    path('resumes/<int:resume_id>/edit-content/', views.content_editor, name='content_editor'),
    path('resumes/<int:resume_id>/download/<str:format_type>/', views.download_resume, name='download_resume'),
    
    # Template and gallery
    path('templates/', views.template_gallery, name='template_gallery'),
    
    # API endpoints
    path('api/resumes/<int:resume_id>/', views.ResumeAPIView.get_resume_data, name='api_resume_data'),
    path('api/resumes/<int:resume_id>/update/', views.ResumeAPIView.update_resume_data, name='api_resume_update'),
    path('api/personal-info/', views.ResumeAPIView.get_personal_info, name='api_personal_info'),
    path('api/personal-info/update/', views.ResumeAPIView.update_personal_info, name='api_personal_info_update'),
    
    # AJAX endpoints
    path('api/experiences/add/', views.add_experience, name='api_add_experience'),
    path('api/projects/add/', views.add_project, name='api_add_project'),
    path('api/competencies/update/', views.update_competencies, name='api_update_competencies'),
]
