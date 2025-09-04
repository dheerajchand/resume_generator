"""
Django services for Resume Generator
Integrates with functional approach
"""

import os
import json
from typing import Dict, Any, List, Optional
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction

from .models import Resume, ResumeTemplate, PersonalInfo, Experience, Project, Education, Certification, Achievement, ColorScheme
from .serializers import ResumeSerializer

# Import our functional modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import ResumeData, ConfigData, load_resume_data, load_config_data, get_default_config
from data_validator import validate_resume_data_complete, enforce_no_placeholders
from style_generator import create_all_styles
from content_manager import ContentManager


class ContentManagementService:
    """Service for managing resume content using functional approach"""
    
    def __init__(self):
        self.content_manager = ContentManager()
    
    def generate_resume_content(self, resume: Resume) -> Dict[str, Any]:
        """Generate resume content using functional approach"""
        try:
            # Get user's data
            personal_info = self._get_personal_info_data(resume.user)
            experience_data = self._get_experience_data(resume.user)
            project_data = self._get_project_data(resume.user)
            education_data = self._get_education_data(resume.user)
            certification_data = self._get_certification_data(resume.user)
            achievement_data = self._get_achievement_data(resume.user)
            competency_data = self._get_competency_data(resume.user)
            
            # Create content using functional approach
            content = {
                'personal_info': personal_info,
                'summary': self._generate_summary(resume.user, resume.template.role),
                'competencies': competency_data,
                'experience': experience_data,
                'projects': project_data,
                'education': education_data,
                'certifications': certification_data,
                'achievements': achievement_data,
                'metadata': {
                    'role': resume.template.role,
                    'version': resume.template.version,
                    'generated_at': resume.created_at.isoformat(),
                    'user': resume.user.username
                }
            }
            
            # Validate content using functional validation
            resume_data = ResumeData(
                personal_info=personal_info,
                summary=content['summary'],
                competencies=competency_data,
                experience=experience_data,
                achievements=achievement_data,
                metadata=content['metadata']
            )
            
            # Enforce no placeholders
            validated_data = enforce_no_placeholders(resume_data)
            
            return content
            
        except Exception as e:
            raise Exception(f"Error generating resume content: {str(e)}")
    
    def _get_personal_info_data(self, user) -> Dict[str, str]:
        """Get personal info data"""
        try:
            personal_info = PersonalInfo.objects.get(user=user)
            return {
                'name': personal_info.full_name,
                'email': personal_info.email,
                'phone': personal_info.phone,
                'website': personal_info.website,
                'linkedin': personal_info.linkedin,
                'github': personal_info.github,
                'location': personal_info.location
            }
        except PersonalInfo.DoesNotExist:
            return {
                'name': user.get_full_name() or user.username,
                'email': user.email,
                'phone': '',
                'website': '',
                'linkedin': '',
                'github': '',
                'location': ''
            }
    
    def _get_experience_data(self, user) -> List[Dict[str, Any]]:
        """Get experience data"""
        experiences = Experience.objects.filter(user=user).order_by('-start_date')
        return [
            {
                'title': exp.title,
                'company': exp.company,
                'location': exp.location,
                'dates': exp.duration,
                'description': exp.description,
                'achievements': exp.achievements,
                'technologies': exp.technologies
            }
            for exp in experiences
        ]
    
    def _get_project_data(self, user) -> List[Dict[str, Any]]:
        """Get project data"""
        projects = Project.objects.filter(user=user).order_by('-start_date')
        return [
            {
                'name': proj.name,
                'description': proj.description,
                'technologies': proj.technologies,
                'url': proj.url,
                'github_url': proj.github_url,
                'impact': proj.impact_description,
                'dates': f"{proj.start_date.year} - {proj.end_date.year if proj.end_date else 'Present'}"
            }
            for proj in projects
        ]
    
    def _get_education_data(self, user) -> List[Dict[str, Any]]:
        """Get education data"""
        educations = Education.objects.filter(user=user).order_by('-start_date')
        return [
            {
                'degree': edu.degree,
                'institution': edu.institution,
                'location': edu.location,
                'dates': f"{edu.start_date.year} - {edu.end_date.year if edu.end_date else 'Present'}",
                'gpa': f"{edu.gpa}/{edu.gpa_scale}" if edu.gpa else None,
                'honors': edu.honors,
                'coursework': edu.relevant_coursework
            }
            for edu in educations
        ]
    
    def _get_certification_data(self, user) -> List[Dict[str, Any]]:
        """Get certification data"""
        certifications = Certification.objects.filter(user=user).order_by('-issue_date')
        return [
            {
                'name': cert.name,
                'issuer': cert.issuer,
                'date': cert.issue_date.strftime('%Y'),
                'expiry': cert.expiry_date.strftime('%Y') if cert.expiry_date else None,
                'credential_id': cert.credential_id,
                'url': cert.credential_url
            }
            for cert in certifications
        ]
    
    def _get_achievement_data(self, user) -> Dict[str, List[str]]:
        """Get achievement data grouped by category"""
        achievements = Achievement.objects.filter(user=user).order_by('-date')
        grouped = {}
        
        for achievement in achievements:
            category = achievement.category
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(achievement.description)
        
        return grouped
    
    def _get_competency_data(self, user) -> Dict[str, List[str]]:
        """Get competency data grouped by category"""
        # This would need to be implemented based on your competency model
        # For now, return empty dict
        return {}
    
    def _generate_summary(self, user, role: str) -> str:
        """Generate professional summary based on role"""
        # Use content manager to get role-specific summary
        template = self.content_manager.get_content_template(role, "long")
        return template.summary
    
    def generate_preview_content(self, resume: Resume) -> Dict[str, Any]:
        """Generate preview content for browser display"""
        content = self.generate_resume_content(resume)
        
        # Add preview-specific formatting
        return {
            'content': content,
            'formatted_html': self._format_for_preview(content)
        }
    
    def _format_for_preview(self, content: Dict[str, Any]) -> str:
        """Format content as HTML for preview"""
        # This would generate HTML preview
        # For now, return basic structure
        return f"<h1>{content['personal_info']['name']}</h1><p>{content['summary']}</p>"


class ResumeGenerationService:
    """Service for generating resume files using functional approach"""
    
    def __init__(self):
        self.content_service = ContentManagementService()
    
    def generate_resume(self, resume: Resume, formats: List[str], color_scheme_id: Optional[int] = None) -> Dict[str, Any]:
        """Generate resume files using functional approach"""
        try:
            # Get content
            content = self.content_service.generate_resume_content(resume)
            
            # Get color scheme
            if color_scheme_id:
                color_scheme = ColorScheme.objects.get(id=color_scheme_id)
                config_data = self._color_scheme_to_config(color_scheme)
            else:
                config_data = get_default_config()
            
            # Generate files
            result_files = {}
            
            for format_type in formats:
                file_path = self._generate_single_format(
                    resume, content, config_data, format_type
                )
                if file_path:
                    result_files[format_type] = file_path
                    
                    # Update resume model with file paths
                    if format_type == 'pdf':
                        resume.pdf_path = file_path
                    elif format_type == 'docx':
                        resume.docx_path = file_path
                    elif format_type == 'rtf':
                        resume.rtf_path = file_path
            
            resume.is_generated = True
            resume.generation_status = 'completed'
            resume.save()
            
            return {
                'success': True,
                'files': result_files
            }
            
        except Exception as e:
            resume.generation_status = 'failed'
            resume.error_message = str(e)
            resume.save()
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def _color_scheme_to_config(self, color_scheme: ColorScheme) -> ConfigData:
        """Convert Django ColorScheme to functional ConfigData"""
        from data_loader import ConfigData
        
        return ConfigData(
            colors=color_scheme.colors,
            typography=color_scheme.typography,
            layout=color_scheme.layout,
            metadata=color_scheme.name
        )
    
    def _generate_single_format(self, resume: Resume, content: Dict[str, Any], 
                               config_data: ConfigData, format_type: str) -> Optional[str]:
        """Generate single format file"""
        try:
            # Create output directory
            output_dir = os.path.join(settings.MEDIA_ROOT, 'resumes', str(resume.id))
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate file based on format
            if format_type == 'pdf':
                return self._generate_pdf(resume, content, config_data, output_dir)
            elif format_type == 'docx':
                return self._generate_docx(resume, content, config_data, output_dir)
            elif format_type == 'rtf':
                return self._generate_rtf(resume, content, config_data, output_dir)
            
        except Exception as e:
            print(f"Error generating {format_type}: {e}")
            return None
    
    def _generate_pdf(self, resume: Resume, content: Dict[str, Any], 
                     config_data: ConfigData, output_dir: str) -> str:
        """Generate PDF using functional approach"""
        # This would use our functional PDF generator
        # For now, create a placeholder
        file_path = os.path.join(output_dir, f"{resume.title}.pdf")
        
        # TODO: Implement actual PDF generation using functional approach
        with open(file_path, 'w') as f:
            f.write("PDF content would be generated here")
        
        return file_path
    
    def _generate_docx(self, resume: Resume, content: Dict[str, Any], 
                      config_data: ConfigData, output_dir: str) -> str:
        """Generate DOCX using functional approach"""
        file_path = os.path.join(output_dir, f"{resume.title}.docx")
        
        # TODO: Implement actual DOCX generation using functional approach
        with open(file_path, 'w') as f:
            f.write("DOCX content would be generated here")
        
        return file_path
    
    def _generate_rtf(self, resume: Resume, content: Dict[str, Any], 
                     config_data: ConfigData, output_dir: str) -> str:
        """Generate RTF using functional approach"""
        file_path = os.path.join(output_dir, f"{resume.title}.rtf")
        
        # TODO: Implement actual RTF generation using functional approach
        with open(file_path, 'w') as f:
            f.write("RTF content would be generated here")
        
        return file_path


class TemplateManagementService:
    """Service for managing resume templates"""
    
    def __init__(self):
        self.content_manager = ContentManager()
    
    def create_resume_from_template(self, user, template: ResumeTemplate, title: str) -> Resume:
        """Create a new resume from template using functional approach"""
        try:
            # Get template content
            template_content = self.content_manager.get_content_template(
                template.role, template.version
            )
            
            # Create resume
            resume = Resume.objects.create(
                user=user,
                template=template,
                title=title,
                content=template_content.__dict__
            )
            
            return resume
            
        except Exception as e:
            raise Exception(f"Error creating resume from template: {str(e)}")
    
    def update_resume_content(self, resume: Resume, content_updates: Dict[str, Any]) -> Resume:
        """Update resume content using functional approach"""
        try:
            # Merge updates with existing content
            current_content = resume.content or {}
            updated_content = self._merge_content(current_content, content_updates)
            
            # Validate content
            resume_data = ResumeData(
                personal_info=updated_content.get('personal_info', {}),
                summary=updated_content.get('summary', ''),
                competencies=updated_content.get('competencies', {}),
                experience=updated_content.get('experience', []),
                achievements=updated_content.get('achievements', {}),
                metadata=updated_content.get('metadata', {})
            )
            
            # Enforce validation
            validated_data = enforce_no_placeholders(resume_data)
            
            # Update resume
            resume.content = updated_content
            resume.save()
            
            return resume
            
        except Exception as e:
            raise Exception(f"Error updating resume content: {str(e)}")
    
    def _merge_content(self, base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """Merge content updates with base content"""
        merged = base.copy()
        
        for key, value in updates.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_content(merged[key], value)
            else:
                merged[key] = value
        
        return merged
