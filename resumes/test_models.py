"""
Test suite for Resume Generator Models
"""

import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import (
    CustomUser, PersonalInfo, UserProfile, UserResumeData, 
    ResumeTemplate, ColorScheme, UserColorScheme
)


class CustomUserModelTests(TestCase):
    """Test the CustomUser model"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'phone': '+1234567890',
            'website': 'https://example.com',
            'linkedin': 'https://linkedin.com/in/testuser',
            'github': 'https://github.com/testuser',
            'location': 'Austin, TX',
            'professional_title': 'Data Scientist',
            'bio': 'Test bio content'
        }
    
    def test_create_custom_user(self):
        """Test creating a custom user with all fields"""
        user = CustomUser.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone, '+1234567890')
        self.assertEqual(user.website, 'https://example.com')
        self.assertEqual(user.linkedin, 'https://linkedin.com/in/testuser')
        self.assertEqual(user.github, 'https://github.com/testuser')
        self.assertEqual(user.location, 'Austin, TX')
        self.assertEqual(user.professional_title, 'Data Scientist')
        self.assertEqual(user.bio, 'Test bio content')
        self.assertEqual(user.preferred_color_scheme, 'default_professional')
        self.assertEqual(user.preferred_resume_length, 'long')
        self.assertFalse(user.is_verified)
        self.assertFalse(user.email_verified)
        self.assertEqual(user.subscription_tier, 'free')
    
    def test_phone_validation(self):
        """Test phone number validation"""
        # Valid phone numbers
        valid_phones = ['+1234567890', '1234567890', '+12345678901234']
        for i, phone in enumerate(valid_phones):
            user_data = self.user_data.copy()
            user_data['phone'] = phone
            user_data['username'] = f'user_{i}'
            user_data['email'] = f'user{i}@example.com'
            user = CustomUser.objects.create_user(**user_data)
            self.assertEqual(user.phone, phone)
    
    def test_user_str_representation(self):
        """Test string representation of user"""
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser (test@example.com)')


class PersonalInfoModelTests(TestCase):
    """Test the PersonalInfo model"""
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.personal_info_data = {
            'user': self.user,
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'website': 'https://johndoe.com',
            'linkedin': 'https://linkedin.com/in/johndoe',
            'github': 'https://github.com/johndoe',
            'location': 'Austin, TX',
            'summary': 'Experienced data scientist with 10+ years...'
        }
    
    def test_create_personal_info(self):
        """Test creating personal info"""
        personal_info = PersonalInfo.objects.create(**self.personal_info_data)
        
        self.assertEqual(personal_info.user, self.user)
        self.assertEqual(personal_info.full_name, 'John Doe')
        self.assertEqual(personal_info.email, 'john@example.com')
        self.assertEqual(personal_info.phone, '+1234567890')
        self.assertEqual(str(personal_info), 'John Doe - Personal Info')
    
    def test_one_to_one_relationship(self):
        """Test that PersonalInfo has one-to-one relationship with User"""
        personal_info = PersonalInfo.objects.create(**self.personal_info_data)
        
        # Test accessing from user
        self.assertEqual(self.user.personal_info, personal_info)


class ColorSchemeModelTests(TestCase):
    """Test the ColorScheme model"""
    
    def setUp(self):
        self.color_scheme_data = {
            'name': 'Test Scheme',
            'description': 'A test color scheme',
            'colors': {
                'primary_color': '#FF0000',
                'secondary_color': '#00FF00',
                'accent_color': '#0000FF',
                'muted_color': '#CCCCCC',
                'background_color': '#FFFFFF',
                'text_color': '#000000'
            },
            'typography': {},
            'layout': {}
        }
    
    def test_create_color_scheme(self):
        """Test creating a color scheme"""
        scheme = ColorScheme.objects.create(**self.color_scheme_data)
        
        self.assertEqual(scheme.name, 'Test Scheme')
        self.assertEqual(scheme.colors['primary_color'], '#FF0000')
        self.assertTrue(scheme.is_active)
        self.assertFalse(scheme.is_default)
        self.assertEqual(str(scheme), 'Test Scheme')


class MultiUserTests(TestCase):
    """Test multi-user functionality"""
    
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        
        self.user2 = CustomUser.objects.create_user(
            username='user2',
            email='user2@example.com', 
            password='pass123'
        )
    
    def test_user_custom_color_schemes(self):
        """Test that users can create custom color schemes"""
        # Create a custom color scheme for user1
        custom_scheme = UserColorScheme.objects.create(
            user=self.user1,
            name='My Custom Scheme',
            slug='my-custom-scheme',
            primary_color='#FF0000',
            secondary_color='#00FF00',
            accent_color='#0000FF',
            muted_color='#CCCCCC'
        )
        
        self.assertEqual(custom_scheme.user, self.user1)
        self.assertEqual(custom_scheme.name, 'My Custom Scheme')
        
        # User2 should not see user1's custom scheme
        user2_schemes = UserColorScheme.objects.filter(user=self.user2)
        self.assertEqual(len(user2_schemes), 0)
    
    def test_user_resume_data_isolation(self):
        """Test that user resume data is properly isolated"""
        # Create resume data for user1
        resume_data1 = UserResumeData.objects.create(
            user=self.user1,
            resume_type='comprehensive',
            length_variant='long',
            personal_info={'name': 'User One'},
            summary='User 1 summary'
        )
        
        # User2 should not see user1's resume data
        user2_resumes = UserResumeData.objects.filter(user=self.user2)
        self.assertEqual(len(user2_resumes), 0)
        
        # User1 should see their own data
        user1_resumes = UserResumeData.objects.filter(user=self.user1)
        self.assertEqual(len(user1_resumes), 1)
        self.assertEqual(user1_resumes[0].summary, 'User 1 summary')
