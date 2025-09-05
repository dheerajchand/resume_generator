"""
Django serializers for Resume Generator
"""

from rest_framework import serializers
from .models import (
    Resume, ResumeTemplate, PersonalInfo, Experience, Project, 
    Education, Certification, Achievement, Competency, CompetencyCategory,
    ColorScheme, ResumeGenerationJob
)


class PersonalInfoSerializer(serializers.ModelSerializer):
    """Serializer for PersonalInfo model"""
    
    class Meta:
        model = PersonalInfo
        fields = [
            'full_name', 'email', 'phone', 'website', 'linkedin', 
            'github', 'location', 'summary'
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for Experience model"""
    
    class Meta:
        model = Experience
        fields = [
            'id', 'title', 'company', 'location', 'start_date', 'end_date',
            'is_current', 'description', 'achievements', 'technologies', 'order'
        ]
        read_only_fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'technologies', 'url', 'github_url',
            'start_date', 'end_date', 'is_current', 'is_highlighted',
            'impact_description', 'order'
        ]
        read_only_fields = ['id']


class EducationSerializer(serializers.ModelSerializer):
    """Serializer for Education model"""
    
    class Meta:
        model = Education
        fields = [
            'id', 'degree', 'institution', 'location', 'start_date', 'end_date',
            'gpa', 'gpa_scale', 'honors', 'relevant_coursework', 'order'
        ]
        read_only_fields = ['id']


class CertificationSerializer(serializers.ModelSerializer):
    """Serializer for Certification model"""
    
    class Meta:
        model = Certification
        fields = [
            'id', 'name', 'issuer', 'issue_date', 'expiry_date',
            'credential_id', 'credential_url', 'is_current', 'order'
        ]
        read_only_fields = ['id']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model"""
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'title', 'description', 'category', 'date',
            'organization', 'url', 'order'
        ]
        read_only_fields = ['id']


class CompetencySerializer(serializers.ModelSerializer):
    """Serializer for Competency model"""
    
    class Meta:
        model = Competency
        fields = [
            'id', 'name', 'proficiency_level', 'years_experience',
            'is_highlighted', 'order'
        ]
        read_only_fields = ['id']


class CompetencyCategorySerializer(serializers.ModelSerializer):
    """Serializer for CompetencyCategory model"""
    competencies = CompetencySerializer(many=True, read_only=True)
    
    class Meta:
        model = CompetencyCategory
        fields = ['id', 'name', 'description', 'order', 'competencies']


class ResumeTemplateSerializer(serializers.ModelSerializer):
    """Serializer for ResumeTemplate model"""
    
    class Meta:
        model = ResumeTemplate
        fields = [
            'id', 'name', 'role', 'version', 'description', 'is_active'
        ]


class ColorSchemeSerializer(serializers.ModelSerializer):
    """Serializer for ColorScheme model"""
    
    class Meta:
        model = ColorScheme
        fields = [
            'id', 'name', 'description', 'colors', 'typography',
            'layout', 'is_default', 'is_active'
        ]


class ResumeSerializer(serializers.ModelSerializer):
    """Serializer for Resume model"""
    template = ResumeTemplateSerializer(read_only=True)
    template_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Resume
        fields = [
            'id', 'title', 'description', 'template', 'template_id',
            'content', 'pdf_path', 'docx_path', 'rtf_path',
            'is_generated', 'generation_status', 'error_message',
            'created_at', 'updated_at', 'generated_at'
        ]
        read_only_fields = [
            'id', 'pdf_path', 'docx_path', 'rtf_path',
            'is_generated', 'generation_status', 'error_message',
            'created_at', 'updated_at', 'generated_at'
        ]


class ResumeGenerationJobSerializer(serializers.ModelSerializer):
    """Serializer for ResumeGenerationJob model"""
    
    class Meta:
        model = ResumeGenerationJob
        fields = [
            'id', 'job_id', 'status', 'formats', 'result_files',
            'error_message', 'created_at', 'started_at', 'completed_at'
        ]
        read_only_fields = ['id', 'job_id', 'created_at', 'started_at', 'completed_at']


class ResumeContentSerializer(serializers.Serializer):
    """Serializer for resume content validation and processing"""
    
    personal_info = PersonalInfoSerializer()
    summary = serializers.CharField()
    competencies = serializers.DictField()
    experience = ExperienceSerializer(many=True)
    projects = ProjectSerializer(many=True)
    education = EducationSerializer(many=True)
    certifications = CertificationSerializer(many=True)
    achievements = AchievementSerializer(many=True)
    
    def validate(self, data):
        """Validate resume content"""
        # Add custom validation logic here
        return data


class ResumeGenerationRequestSerializer(serializers.Serializer):
    """Serializer for resume generation requests"""
    
    formats = serializers.ListField(
        child=serializers.ChoiceField(choices=['pdf', 'docx', 'rtf']),
        default=['pdf']
    )
    color_scheme_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_formats(self, value):
        """Validate formats list"""
        if not value:
            raise serializers.ValidationError("At least one format must be specified")
        return value


class ResumePreviewSerializer(serializers.Serializer):
    """Serializer for resume preview data"""
    
    content = ResumeContentSerializer()
    formatted_html = serializers.CharField()
    template_info = ResumeTemplateSerializer()
    color_scheme = ColorSchemeSerializer()
    
    class Meta:
        fields = ['content', 'formatted_html', 'template_info', 'color_scheme']
