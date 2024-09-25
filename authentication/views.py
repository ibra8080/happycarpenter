import logging
from dj_rest_auth.registration.views import RegisterView
from .serializers import RegisterSerializer

logger = logging.getLogger(__name__)

class CustomRegisterView(RegisterView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f"Received registration data: {request.data}")
        return super().create(request, *args, **kwargs)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user_data = serializer.save()
                logger.info(f"User created successfully: {user_data['user'].username}")
                return Response({
                    "user": {
                        "username": user_data['user'].username,
                        "email": user_data['user'].email,
                        "first_name": user_data['user'].first_name,
                        "last_name": user_data['user'].last_name,
                    },
                    "profile": ProfileSerializer(user_data['profile']).data,
                    "refresh": user_data['refresh'],
                    "access": user_data['access']
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating user: {str(e)}")
                return Response({
                    "error": "An error occurred while creating the user."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Invalid registration data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
