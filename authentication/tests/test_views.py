from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from profiles.models import Profile

class RegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'  # Adjust this to your actual registration URL

    def test_successful_amateur_registration(self):
        data = {
            "username": "amateuruser",
            "email": "amateur@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "Amateur",
            "last_name": "User",
            "user_type": "amateur",
            "interests": ["woodworking", "painting"]
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="amateuruser").exists())
        self.assertTrue(Profile.objects.filter(owner__username="amateuruser").exists())
        self.assertEqual(Profile.objects.get(owner__username="amateuruser").user_type, "amateur")

    def test_successful_professional_registration(self):
        data = {
            "username": "prouser",
            "email": "pro@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "Pro",
            "last_name": "User",
            "user_type": "professional",
            "years_of_experience": 5,
            "specialties": "Carpentry",
            "portfolio_url": "https://example.com/portfolio"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="prouser").exists())
        self.assertTrue(Profile.objects.filter(owner__username="prouser").exists())
        self.assertEqual(Profile.objects.get(owner__username="prouser").user_type, "professional")

    def test_invalid_registration(self):
        data = {
            "username": "invaliduser",
            "email": "invalid@example.com",
            "password1": "password123",
            "password2": "password456",  # Mismatched passwords
            "user_type": "professional",
            # Missing required fields for professional
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="invaliduser").exists())
