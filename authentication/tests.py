from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class AuthenticationTests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='testpass123'
        )
        
        # URLs
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.profile_url = reverse('profile-list')  # Adjust this to match your URL configuration

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'user_type': 'amateur'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_user_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_token_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        data = {'refresh': str(refresh)}
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_access_protected_resource(self):
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_resource_without_token(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_registration(self):
        # Test with mismatched passwords
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'differentpass',
            'first_name': 'New',
            'last_name': 'User',
            'user_type': 'amateur'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_login(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
