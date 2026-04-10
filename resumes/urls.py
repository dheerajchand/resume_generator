"""
URL configuration for resumes app
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Create router for API viewsets
router = DefaultRouter()
router.register(r'resume-data', views.UserResumeDataViewSet, basename='resume-data')
router.register(r'resumes', views.ResumeViewSet, basename='resumes')
router.register(r'color-schemes', views.ColorSchemeViewSet, basename='color-schemes')
router.register(r'user-color-schemes', views.UserColorSchemeViewSet, basename='user-color-schemes')
router.register(r'generation-jobs', views.ResumeGenerationJobViewSet, basename='generation-jobs')

app_name = 'resumes'

urlpatterns = [
    # Public pages — no login required
    path('', views.download_form, name='download_form'),
    path('download/', views.generate_on_demand, name='generate_on_demand'),

    # Authenticated views
    path('download/instance/<int:instance_id>/', views.generate_instance, name='generate_instance'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:resume_id>/download/<str:format_type>/', views.download_resume, name='download_resume'),

    # API endpoints
    path('api/', include(router.urls)),
    path('api/generate/', views.generate_resume, name='generate_resume'),
]
