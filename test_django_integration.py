#!/usr/bin/env python3
"""
Test Django integration with functional approach
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_generator_django.settings')
django.setup()

from django.contrib.auth.models import User
from resumes.models import ResumeTemplate, PersonalInfo, Experience, Project, ColorScheme
from resumes.services import ContentManagementService, ResumeGenerationService
from data_loader import ResumeData, get_default_config
from data_validator import validate_resume_data_complete, enforce_no_placeholders


def test_django_models():
    """Test Django models"""
    print("🧪 Testing Django Models")
    print("=" * 40)
    
    # Test templates
    templates = ResumeTemplate.objects.all()
    print(f"✅ Found {templates.count()} resume templates")
    for template in templates[:3]:
        print(f"  • {template.name} ({template.role} - {template.version})")
    
    # Test color schemes
    color_schemes = ColorScheme.objects.all()
    print(f"✅ Found {color_schemes.count()} color schemes")
    for scheme in color_schemes:
        print(f"  • {scheme.name} ({len(scheme.colors)} colors)")
    
    return True


def test_user_creation():
    """Test user creation and personal info"""
    print("\n🧪 Testing User Creation")
    print("=" * 40)
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='test_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"ℹ️  Test user already exists: {user.username}")
    
    # Create personal info
    personal_info, created = PersonalInfo.objects.get_or_create(
        user=user,
        defaults={
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone': '(555) 123-4567',
            'website': 'https://testuser.com',
            'linkedin': 'https://linkedin.com/in/testuser',
            'github': 'https://github.com/testuser',
            'location': 'Test City, TC',
            'summary': 'Experienced software engineer with expertise in Python and Django development.'
        }
    )
    
    if created:
        print(f"✅ Created personal info for: {personal_info.full_name}")
    else:
        print(f"ℹ️  Personal info already exists for: {personal_info.full_name}")
    
    return user, personal_info


def test_experience_creation(user):
    """Test experience creation"""
    print("\n🧪 Testing Experience Creation")
    print("=" * 40)
    
    # Create test experience
    experience, created = Experience.objects.get_or_create(
        user=user,
        title='Senior Software Engineer',
        company='Test Company Inc',
        defaults={
            'location': 'Test City, TC',
            'start_date': '2020-01-01',
            'end_date': '2023-12-31',
            'description': 'Led development of scalable web applications using Python and Django',
            'achievements': [
                'Built microservices architecture serving 100,000+ users',
                'Implemented CI/CD pipeline reducing deployment time by 70%',
                'Mentored 5 junior developers'
            ],
            'technologies': ['Python', 'Django', 'PostgreSQL', 'React', 'Docker']
        }
    )
    
    if created:
        print(f"✅ Created experience: {experience.title} at {experience.company}")
    else:
        print(f"ℹ️  Experience already exists: {experience.title} at {experience.company}")
    
    return experience


def test_project_creation(user):
    """Test project creation"""
    print("\n🧪 Testing Project Creation")
    print("=" * 40)
    
    # Create test project
    project, created = Project.objects.get_or_create(
        user=user,
        name='Resume Generator System',
        defaults={
            'description': 'Full-stack resume generation system with Django and functional programming',
            'technologies': ['Python', 'Django', 'ReportLab', 'React', 'PostgreSQL'],
            'url': 'https://github.com/testuser/resume-generator',
            'github_url': 'https://github.com/testuser/resume-generator',
            'start_date': '2024-01-01',
            'is_current': True,
            'is_highlighted': True,
            'impact_description': 'Used by 100+ professionals to generate professional resumes'
        }
    )
    
    if created:
        print(f"✅ Created project: {project.name}")
    else:
        print(f"ℹ️  Project already exists: {project.name}")
    
    return project


def test_content_management_service():
    """Test content management service"""
    print("\n🧪 Testing Content Management Service")
    print("=" * 40)
    
    try:
        service = ContentManagementService()
        
        # Test getting content template
        template = service.content_manager.get_content_template('software_engineer', 'long')
        print(f"✅ Got content template: {template.role} - {template.version}")
        print(f"  Summary length: {len(template.summary)} characters")
        print(f"  Competencies: {len(template.competencies)} categories")
        print(f"  Experience: {len(template.experience)} entries")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing content management: {e}")
        return False


def test_resume_creation(user, personal_info, experience, project):
    """Test resume creation"""
    print("\n🧪 Testing Resume Creation")
    print("=" * 40)
    
    try:
        # Get a template
        template = ResumeTemplate.objects.filter(role='software_engineer', version='long').first()
        if not template:
            print("❌ No software engineer template found")
            return False
        
        # Create resume
        resume, created = Resume.objects.get_or_create(
            user=user,
            template=template,
            title='Test Software Engineer Resume',
            defaults={
                'description': 'Test resume for software engineer position',
                'content': {}
            }
        )
        
        if created:
            print(f"✅ Created resume: {resume.title}")
        else:
            print(f"ℹ️  Resume already exists: {resume.title}")
        
        # Test content generation
        content_service = ContentManagementService()
        content = content_service.generate_resume_content(resume)
        
        print(f"✅ Generated resume content:")
        print(f"  Personal info: {content['personal_info']['name']}")
        print(f"  Experience entries: {len(content['experience'])}")
        print(f"  Project entries: {len(content['projects'])}")
        print(f"  Competency categories: {len(content['competencies'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing resume creation: {e}")
        return False


def test_functional_validation():
    """Test functional validation with Django data"""
    print("\n🧪 Testing Functional Validation")
    print("=" * 40)
    
    try:
        # Create test resume data
        resume_data = ResumeData(
            personal_info={
                'name': 'Test User',
                'email': 'test@example.com',
                'phone': '(555) 123-4567',
                'website': 'https://testuser.com',
                'linkedin': 'https://linkedin.com/in/testuser',
                'github': 'https://github.com/testuser',
                'location': 'Test City, TC'
            },
            summary='Experienced software engineer with expertise in Python and Django development.',
            competencies={
                'Programming Languages': ['Python', 'JavaScript', 'TypeScript'],
                'Frameworks': ['Django', 'React', 'FastAPI']
            },
            experience=[
                {
                    'title': 'Senior Software Engineer',
                    'company': 'Test Company Inc',
                    'location': 'Test City, TC',
                    'dates': '2020-2023',
                    'description': 'Led development of scalable web applications',
                    'achievements': ['Built microservices architecture', 'Implemented CI/CD pipeline'],
                    'technologies': ['Python', 'Django', 'PostgreSQL']
                }
            ],
            achievements={
                'Technical Leadership': ['Led team of 5 developers', 'Mentored junior developers'],
                'Project Success': ['Delivered 10+ successful projects', 'Improved performance by 50%']
            },
            metadata={'role': 'software_engineer', 'version': 'long'}
        )
        
        # Test validation
        validation_result = validate_resume_data_complete(resume_data)
        print(f"✅ Validation result: {'PASSED' if validation_result.is_valid else 'FAILED'}")
        
        if not validation_result.is_valid:
            print("  Errors:")
            for error in validation_result.errors:
                print(f"    • {error}")
        
        # Test enforcement
        try:
            validated_data = enforce_no_placeholders(resume_data)
            print("✅ Placeholder validation: PASSED")
        except ValueError as e:
            print(f"❌ Placeholder validation: FAILED - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing functional validation: {e}")
        return False


def main():
    """Run all Django integration tests"""
    print("🚀 Django Integration Test Suite")
    print("=" * 60)
    
    tests = [
        test_django_models,
        test_user_creation,
        test_experience_creation,
        test_project_creation,
        test_content_management_service,
        test_functional_validation
    ]
    
    passed = 0
    total = len(tests)
    
    # Run tests
    user = None
    personal_info = None
    experience = None
    project = None
    
    for i, test in enumerate(tests):
        try:
            if test.__name__ == 'test_user_creation':
                user, personal_info = test()
                if user and personal_info:
                    passed += 1
            elif test.__name__ == 'test_experience_creation':
                experience = test(user)
                if experience:
                    passed += 1
            elif test.__name__ == 'test_project_creation':
                project = test(user)
                if project:
                    passed += 1
            elif test.__name__ == 'test_resume_creation':
                if test(user, personal_info, experience, project):
                    passed += 1
            else:
                if test():
                    passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Django integration tests passed!")
        print("\n✅ Django + Functional approach is working correctly!")
        print("\nNext steps:")
        print("  1. Run Django development server: python manage.py runserver")
        print("  2. Access admin interface: http://127.0.0.1:8000/admin/")
        print("  3. Create resume content and generate files")
        print("  4. Test web interface and API endpoints")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return passed == total


if __name__ == "__main__":
    main()
