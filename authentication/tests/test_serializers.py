from django.test import TestCase
from authentication.serializers import RegisterSerializer

class RegisterSerializerTestCase(TestCase):
    def test_valid_amateur_data(self):
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
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_professional_data(self):
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
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_mismatched_passwords(self):
        data = {
            "username": "invaliduser",
            "email": "invalid@example.com",
            "password1": "password123",
            "password2": "password456",
            "user_type": "amateur"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_invalid_professional_data_missing_fields(self):
        data = {
            "username": "incompletepro",
            "email": "incomplete@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "user_type": "professional"
            # Missing required fields for professional
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('years_of_experience', serializer.errors)
        self.assertIn('specialties', serializer.errors)
