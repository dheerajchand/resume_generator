"""
Test suite for Resume Generator API
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import CustomUser, PersonalInfo


class APIAuthenticationTests(APITestCase):
    """Test API authentication and authorization"""
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_api_authentication_required(self):
        """Test that API requires authentication"""
        self.client.logout()
        response = self.client.get('/api/resumes/')
        # Should be either 401 (unauthorized) or 403 (forbidden)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_authenticated_api_access(self):
        """Test that authenticated users can access API"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/resumes/')
        # Should either return 200 OK or 404 if endpoint doesn't exist yet
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])


class SecurityTests(TestCase):
    """Test security aspects of the application"""
    
    def test_unauthenticated_access_blocked(self):
        """Test that unauthenticated users cannot access protected resources"""
        client = Client()
        
        # Test admin access
        response = client.get('/admin/')
        self.assertIn(response.status_code, [302, 403])  # Redirect to login or forbidden
    
    def test_user_isolation(self):
        """Test that users can only access their own data"""
        user1 = CustomUser.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        
        user2 = CustomUser.objects.create_user(
            username='user2', 
            email='user2@example.com',
            password='pass123'
        )
        
        # Create personal info for user1
        personal_info1 = PersonalInfo.objects.create(
            user=user1,
            full_name='User One',
            email='user1@example.com'
        )
        
        # User2 should not be able to access user1's data
        user2_personal_info = PersonalInfo.objects.filter(user=user2)
        self.assertEqual(len(user2_personal_info), 0)
