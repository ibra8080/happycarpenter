import logging
from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView
from .serializers import RegisterSerializer
from profiles.serializers import ProfileSerializer

logger = logging.getLogger(__name__)

class CustomRegisterView(RegisterView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f"Received registration data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                data = self.get_response_data(user)
                return Response(data, status=status.HTTP_201_CREATED, headers=headers)
            except Exception as e:
                logger.exception(f"Detailed error creating user: {str(e)}")
                return Response({
                    "error": f"An error occurred while creating the user: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Invalid registration data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def get_response_data(self, user):
        return {
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "profile": ProfileSerializer(user.profile).data,
        }