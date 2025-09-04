"""
Django management command to set up the resume generation system
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from resumes.models import (
    ResumeTemplate, CompetencyCategory, Competency, ColorScheme
)
from resumes.services import ContentManagementService
import json
import os


class Command(BaseCommand):
    help = 'Set up the resume generation system with templates, competencies, and color schemes'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser account',
        )
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for superuser',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email for superuser',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password for superuser',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Setting up Resume Generation System'))
        
        # Create superuser if requested
        if options['create_superuser']:
            self.create_superuser(options)
        
        # Set up templates
        self.setup_templates()
        
        # Set up competency categories
        self.setup_competency_categories()
        
        # Set up color schemes
        self.setup_color_schemes()
        
        # Set up content management
        self.setup_content_management()
        
        self.stdout.write(self.style.SUCCESS('✅ Resume system setup complete!'))
    
    def create_superuser(self, options):
        """Create superuser account"""
        self.stdout.write('Creating superuser...')
        
        if User.objects.filter(username=options['username']).exists():
            self.stdout.write(f'Superuser {options["username"]} already exists')
            return
        
        User.objects.create_superuser(
            username=options['username'],
            email=options['email'],
            password=options['password']
        )
        
        self.stdout.write(f'✅ Created superuser: {options["username"]}')
    
    def setup_templates(self):
        """Set up resume templates"""
        self.stdout.write('Setting up resume templates...')
        
        templates = [
            {
                'name': 'Software Engineer - Long',
                'role': 'software_engineer',
                'version': 'long',
                'description': 'Comprehensive software engineer resume with full experience details'
            },
            {
                'name': 'Software Engineer - Short',
                'role': 'software_engineer',
                'version': 'short',
                'description': 'Concise software engineer resume (1-2 pages)'
            },
            {
                'name': 'Data Scientist - Long',
                'role': 'data_scientist',
                'version': 'long',
                'description': 'Comprehensive data scientist resume with research focus'
            },
            {
                'name': 'Data Scientist - Short',
                'role': 'data_scientist',
                'version': 'short',
                'description': 'Concise data scientist resume'
            },
            {
                'name': 'Research Analyst - Long',
                'role': 'research_analyst',
                'version': 'long',
                'description': 'Comprehensive research analyst resume with publications'
            },
            {
                'name': 'Research Analyst - Short',
                'role': 'research_analyst',
                'version': 'short',
                'description': 'Concise research analyst resume'
            },
            {
                'name': 'General - Long',
                'role': 'general',
                'version': 'long',
                'description': 'General purpose comprehensive resume'
            },
            {
                'name': 'General - Short',
                'role': 'general',
                'version': 'short',
                'description': 'General purpose concise resume'
            },
        ]
        
        for template_data in templates:
            template, created = ResumeTemplate.objects.get_or_create(
                role=template_data['role'],
                version=template_data['version'],
                defaults=template_data
            )
            
            if created:
                self.stdout.write(f'  ✅ Created template: {template.name}')
            else:
                self.stdout.write(f'  ℹ️  Template already exists: {template.name}')
    
    def setup_competency_categories(self):
        """Set up competency categories and skills"""
        self.stdout.write('Setting up competency categories...')
        
        categories_data = [
            {
                'name': 'Programming Languages',
                'description': 'Programming and scripting languages',
                'order': 1,
                'competencies': [
                    ('Python', 'expert', 8),
                    ('JavaScript', 'advanced', 6),
                    ('TypeScript', 'advanced', 4),
                    ('R', 'advanced', 7),
                    ('SQL', 'expert', 10),
                    ('Scala', 'intermediate', 3),
                    ('Java', 'intermediate', 4),
                    ('Go', 'beginner', 1),
                ]
            },
            {
                'name': 'Frameworks & Libraries',
                'description': 'Web frameworks and development libraries',
                'order': 2,
                'competencies': [
                    ('Django', 'expert', 8),
                    ('Flask', 'advanced', 6),
                    ('React', 'advanced', 5),
                    ('Node.js', 'intermediate', 4),
                    ('Express.js', 'intermediate', 3),
                    ('FastAPI', 'advanced', 3),
                    ('Pandas', 'expert', 8),
                    ('NumPy', 'expert', 8),
                    ('Scikit-learn', 'advanced', 6),
                    ('TensorFlow', 'intermediate', 3),
                ]
            },
            {
                'name': 'Cloud & Infrastructure',
                'description': 'Cloud platforms and infrastructure tools',
                'order': 3,
                'competencies': [
                    ('AWS', 'advanced', 5),
                    ('Google Cloud', 'intermediate', 3),
                    ('Docker', 'advanced', 4),
                    ('Kubernetes', 'intermediate', 2),
                    ('Terraform', 'beginner', 1),
                    ('CI/CD', 'advanced', 4),
                    ('Apache Spark', 'advanced', 5),
                    ('Apache Kafka', 'intermediate', 3),
                ]
            },
            {
                'name': 'Databases & Data',
                'description': 'Database systems and data processing',
                'order': 4,
                'competencies': [
                    ('PostgreSQL', 'expert', 8),
                    ('MongoDB', 'advanced', 5),
                    ('Redis', 'intermediate', 3),
                    ('MySQL', 'advanced', 6),
                    ('Oracle', 'intermediate', 4),
                    ('ETL/ELT', 'expert', 7),
                    ('Data Warehousing', 'advanced', 5),
                ]
            },
            {
                'name': 'Data Science & Analytics',
                'description': 'Data science and analytical tools',
                'order': 5,
                'competencies': [
                    ('Machine Learning', 'advanced', 6),
                    ('Statistical Analysis', 'expert', 8),
                    ('Data Visualization', 'expert', 7),
                    ('Tableau', 'advanced', 5),
                    ('PowerBI', 'intermediate', 3),
                    ('D3.js', 'intermediate', 3),
                    ('Matplotlib', 'expert', 7),
                    ('Seaborn', 'advanced', 6),
                ]
            },
            {
                'name': 'Research & Methodology',
                'description': 'Research methods and analytical approaches',
                'order': 6,
                'competencies': [
                    ('Survey Design', 'expert', 8),
                    ('Sampling Methodology', 'expert', 7),
                    ('Experimental Design', 'advanced', 5),
                    ('Qualitative Research', 'intermediate', 4),
                    ('Program Evaluation', 'advanced', 6),
                    ('Policy Analysis', 'advanced', 5),
                ]
            }
        ]
        
        for category_data in categories_data:
            category, created = CompetencyCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'order': category_data['order']
                }
            )
            
            if created:
                self.stdout.write(f'  ✅ Created category: {category.name}')
            else:
                self.stdout.write(f'  ℹ️  Category already exists: {category.name}')
            
            # Add competencies
            for comp_name, proficiency, years in category_data['competencies']:
                competency, created = Competency.objects.get_or_create(
                    category=category,
                    name=comp_name,
                    defaults={
                        'proficiency_level': proficiency,
                        'years_experience': years,
                        'order': len(category.competencies.all())
                    }
                )
                
                if created:
                    self.stdout.write(f'    ✅ Added competency: {comp_name}')
    
    def setup_color_schemes(self):
        """Set up color schemes"""
        self.stdout.write('Setting up color schemes...')
        
        color_schemes = [
            {
                'name': 'Professional Blue',
                'description': 'Clean, professional blue color scheme',
                'colors': {
                    'NAME_COLOR': '#1F4E79',
                    'TITLE_COLOR': '#2E5090',
                    'SECTION_HEADER_COLOR': '#2E5090',
                    'JOB_TITLE_COLOR': '#4682B4',
                    'ACCENT_COLOR': '#4682B4',
                    'COMPETENCY_HEADER_COLOR': '#1F4E79',
                    'SUBTITLE_COLOR': '#1F4E79',
                    'LINK_COLOR': '#2E5090',
                    'DARK_TEXT_COLOR': '#333333',
                    'MEDIUM_TEXT_COLOR': '#666666',
                    'LIGHT_TEXT_COLOR': '#999999'
                },
                'typography': {
                    'FONT_MAIN': 'Helvetica',
                    'FONT_BOLD': 'Helvetica-Bold',
                    'FONT_ITALIC': 'Helvetica-Oblique',
                    'NAME_SIZE': 24,
                    'TITLE_SIZE': 14,
                    'SECTION_HEADER_SIZE': 12,
                    'JOB_TITLE_SIZE': 11,
                    'BODY_SIZE': 9,
                    'CONTACT_SIZE': 9
                },
                'layout': {
                    'PAGE_MARGIN': 0.6,
                    'SECTION_SPACING': 0.12,
                    'PARAGRAPH_SPACING': 0.06,
                    'LINE_SPACING': 1.15,
                    'JOB_SPACING': 6,
                    'CATEGORY_SPACING': 4,
                    'MAX_PAGES': 2,
                    'BULLET_CHAR': '▸'
                },
                'is_default': True
            },
            {
                'name': 'Modern Tech',
                'description': 'Modern, tech-focused color scheme',
                'colors': {
                    'NAME_COLOR': '#2C3E50',
                    'TITLE_COLOR': '#E74C3C',
                    'SECTION_HEADER_COLOR': '#E74C3C',
                    'JOB_TITLE_COLOR': '#3498DB',
                    'ACCENT_COLOR': '#3498DB',
                    'COMPETENCY_HEADER_COLOR': '#2C3E50',
                    'SUBTITLE_COLOR': '#2C3E50',
                    'LINK_COLOR': '#E74C3C',
                    'DARK_TEXT_COLOR': '#2C3E50',
                    'MEDIUM_TEXT_COLOR': '#7F8C8D',
                    'LIGHT_TEXT_COLOR': '#BDC3C7'
                },
                'typography': {
                    'FONT_MAIN': 'Helvetica',
                    'FONT_BOLD': 'Helvetica-Bold',
                    'FONT_ITALIC': 'Helvetica-Oblique',
                    'NAME_SIZE': 26,
                    'TITLE_SIZE': 16,
                    'SECTION_HEADER_SIZE': 13,
                    'JOB_TITLE_SIZE': 12,
                    'BODY_SIZE': 10,
                    'CONTACT_SIZE': 9
                },
                'layout': {
                    'PAGE_MARGIN': 0.7,
                    'SECTION_SPACING': 0.15,
                    'PARAGRAPH_SPACING': 0.08,
                    'LINE_SPACING': 1.2,
                    'JOB_SPACING': 8,
                    'CATEGORY_SPACING': 5,
                    'MAX_PAGES': 2,
                    'BULLET_CHAR': '▶'
                }
            },
            {
                'name': 'Academic Green',
                'description': 'Academic and research-focused color scheme',
                'colors': {
                    'NAME_COLOR': '#228B22',
                    'TITLE_COLOR': '#B8860B',
                    'SECTION_HEADER_COLOR': '#B8860B',
                    'JOB_TITLE_COLOR': '#722F37',
                    'ACCENT_COLOR': '#722F37',
                    'COMPETENCY_HEADER_COLOR': '#228B22',
                    'SUBTITLE_COLOR': '#228B22',
                    'LINK_COLOR': '#B8860B',
                    'DARK_TEXT_COLOR': '#333333',
                    'MEDIUM_TEXT_COLOR': '#666666',
                    'LIGHT_TEXT_COLOR': '#999999'
                },
                'typography': {
                    'FONT_MAIN': 'Times New Roman',
                    'FONT_BOLD': 'Times New Roman Bold',
                    'FONT_ITALIC': 'Times New Roman Italic',
                    'NAME_SIZE': 24,
                    'TITLE_SIZE': 14,
                    'SECTION_HEADER_SIZE': 12,
                    'JOB_TITLE_SIZE': 11,
                    'BODY_SIZE': 9,
                    'CONTACT_SIZE': 9
                },
                'layout': {
                    'PAGE_MARGIN': 0.6,
                    'SECTION_SPACING': 0.12,
                    'PARAGRAPH_SPACING': 0.06,
                    'LINE_SPACING': 1.15,
                    'JOB_SPACING': 6,
                    'CATEGORY_SPACING': 4,
                    'MAX_PAGES': 3,
                    'BULLET_CHAR': '•'
                }
            }
        ]
        
        for scheme_data in color_schemes:
            scheme, created = ColorScheme.objects.get_or_create(
                name=scheme_data['name'],
                defaults=scheme_data
            )
            
            if created:
                self.stdout.write(f'  ✅ Created color scheme: {scheme.name}')
            else:
                self.stdout.write(f'  ℹ️  Color scheme already exists: {scheme.name}')
    
    def setup_content_management(self):
        """Set up content management system"""
        self.stdout.write('Setting up content management...')
        
        # Create content directories
        content_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'content')
        os.makedirs(content_dir, exist_ok=True)
        os.makedirs(os.path.join(content_dir, 'role_overrides'), exist_ok=True)
        
        # Initialize content manager
        content_service = ContentManagementService()
        
        self.stdout.write('  ✅ Content management system initialized')
        self.stdout.write('  ✅ Content directories created')
        
        # Create logs directory
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        self.stdout.write('  ✅ Logs directory created')
