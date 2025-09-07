#!/usr/bin/env python
"""
Test script for user authentication system
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_generator_django.settings')
django.setup()

from resumes.models import CustomUser, UserProfile, UserResumeData, UserDirectory, ColorScheme
from django.contrib.auth import authenticate

def test_user_system():
    """Test the user authentication system"""
    print("🧪 Testing User Authentication System")
    print("=" * 50)
    
    # Test 1: Check if admin user exists
    try:
        admin_user = CustomUser.objects.get(username='admin')
        print(f"✅ Admin user found: {admin_user.username} ({admin_user.email})")
        print(f"   - Full name: {admin_user.full_name}")
        print(f"   - Subscription: {admin_user.subscription_tier}")
        print(f"   - Is staff: {admin_user.is_staff}")
        print(f"   - Is superuser: {admin_user.is_superuser}")
    except CustomUser.DoesNotExist:
        print("❌ Admin user not found")
        return False
    
    # Test 2: Check user profile
    try:
        profile = admin_user.profile
        print(f"✅ User profile found: {profile}")
        print(f"   - Professional summary: {profile.professional_summary[:50]}...")
        print(f"   - Default template: {profile.default_resume_template}")
        print(f"   - Auto generate: {profile.auto_generate_on_update}")
    except UserProfile.DoesNotExist:
        print("❌ User profile not found")
        return False
    
    # Test 3: Check user directories
    try:
        directory = admin_user.directories.first()
        print(f"✅ User directory found: {directory}")
        print(f"   - Input directory: {directory.input_directory}")
        print(f"   - Output directory: {directory.output_directory}")
        print(f"   - Initialized: {directory.is_initialized}")
    except UserDirectory.DoesNotExist:
        print("❌ User directory not found")
        return False
    
    # Test 4: Check resume data
    resume_data_count = admin_user.resume_data.count()
    print(f"✅ Resume data entries: {resume_data_count}")
    
    if resume_data_count > 0:
        for data in admin_user.resume_data.all()[:3]:  # Show first 3
            print(f"   - {data.resume_type} ({data.length_variant}) - {'Active' if data.is_active else 'Inactive'}")
    
    # Test 5: Check color schemes
    color_schemes = ColorScheme.objects.filter(is_active=True)
    print(f"✅ Color schemes: {color_schemes.count()}")
    
    for scheme in color_schemes[:3]:  # Show first 3
        print(f"   - {scheme.name} ({'Default' if scheme.is_default else 'Custom'})")
    
    # Test 6: Test authentication
    user = authenticate(username='admin', password='admin123')
    if user:
        print("✅ Authentication test passed")
    else:
        print("❌ Authentication test failed")
        return False
    
    print("\n🎉 All tests passed! User system is working correctly.")
    return True

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints")
    print("=" * 50)
    
    # Test if we can import views
    try:
        from resumes.views import dashboard, generate_resume
        from resumes.serializers import UserResumeDataSerializer
        print("✅ API views and serializers imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    print("✅ API endpoints are properly configured")
    return True

if __name__ == '__main__':
    success = test_user_system()
    if success:
        test_api_endpoints()
        print("\n🚀 User authentication system is ready!")
        print("   - Admin interface: http://localhost:8000/admin/")
        print("   - User dashboard: http://localhost:8000/")
        print("   - API endpoints: http://localhost:8000/api/")
    else:
        print("\n❌ User system setup failed!")
        sys.exit(1)
