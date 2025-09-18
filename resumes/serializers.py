"""
Serializers for Resume Generator API
"""

from rest_framework import serializers
from .models import (
    CustomUser, UserProfile, UserResumeData, UserDirectory,
    Resume, ResumeTemplate, ColorScheme, UserColorScheme, ResumeGenerationJob
)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile"""
    
    class Meta:
        model = UserProfile
        fields = [
            'professional_summary', 'show_phone', 'show_email', 'show_website',
            'show_linkedin', 'show_github', 'default_resume_template',
            'auto_generate_on_update', 'profile_public', 'allow_public_resumes'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'website', 'linkedin', 'github', 'location',
            'professional_title', 'bio', 'preferred_color_scheme',
            'preferred_resume_length', 'is_verified', 'email_verified',
            'subscription_tier', 'date_joined', 'last_login', 'profile'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserResumeDataSerializer(serializers.ModelSerializer):
    """Serializer for UserResumeData"""
    
    class Meta:
        model = UserResumeData
        fields = [
            'id', 'resume_type', 'length_variant', 'personal_info',
            'summary', 'competencies', 'experience', 'achievements',
            'education', 'projects', 'certifications', 'additional_info',
            'is_active', 'last_generated', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_generated']


class ResumeTemplateSerializer(serializers.ModelSerializer):
    """Serializer for ResumeTemplate"""
    
    class Meta:
        model = ResumeTemplate
        fields = [
            'id', 'name', 'role', 'version', 'description',
            'is_active', 'created_at', 'updated_at'
        ]


class ColorSchemeSerializer(serializers.ModelSerializer):
    """Serializer for ColorScheme"""
    
    class Meta:
        model = ColorScheme
        fields = [
            'id', 'name', 'description', 'colors', 'typography',
            'layout', 'is_default', 'is_active', 'created_at', 'updated_at'
        ]


class ResumeSerializer(serializers.ModelSerializer):
    """Serializer for Resume"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Resume
        fields = [
            'id', 'template', 'template_name', 'user_name', 'title',
            'description', 'content', 'pdf_path', 'docx_path', 'rtf_path',
            'is_generated', 'generation_status', 'error_message',
            'created_at', 'updated_at', 'generated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'generated_at',
            'pdf_path', 'docx_path', 'rtf_path'
        ]


class UserColorSchemeSerializer(serializers.ModelSerializer):
    """Serializer for UserColorScheme"""
    
    class Meta:
        model = UserColorScheme
        fields = [
            'id', 'name', 'slug', 'description', 'primary_color',
            'secondary_color', 'accent_color', 'muted_color',
            'background_color', 'text_color', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Automatically assign the current user when creating"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ResumeGenerationJobSerializer(serializers.ModelSerializer):
    """Serializer for ResumeGenerationJob"""
    resume_title = serializers.CharField(source='resume.title', read_only=True)
    color_scheme_name = serializers.CharField(source='color_scheme.name', read_only=True)
    
    class Meta:
        model = ResumeGenerationJob
        fields = [
            'id', 'job_id', 'resume', 'resume_title', 'status',
            'formats', 'color_scheme', 'color_scheme_name',
            'result_files', 'error_message', 'created_at',
            'started_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'job_id', 'created_at', 'started_at', 'completed_at'
        ]