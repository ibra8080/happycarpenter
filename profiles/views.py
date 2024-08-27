from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from happy_carpenter_api.permissions import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
import logging

logger = logging.getLogger(__name__)


class ProfileList(APIView):
    """
    List all profiles
    No Create view (post method), as profile creation handled by django signals
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            logger.warning(f"Profile not found for pk: {pk}")
            raise Http404

    def get(self, request, pk):
        try:
            profile = self.get_object(pk)
            serializer = ProfileSerializer(
                profile, context={'request': request}
            )
            logger.info(f"Profile retrieved successfully for pk: {pk}")
            return Response(serializer.data)
        except Http404:
            logger.warning(f"Profile not found for pk: {pk}")
            return Response(
                {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in ProfileDetail get: {str(e)}")
            return Response(
                    {"detail": "An error occurred."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, data=request.data, context={
                'request': request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Profile updated successfully for pk: {pk}")
            return Response(serializer.data)
        logger.warning(f"Invalid data for profile update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.delete()
        logger.info(f"Profile deleted successfully for pk: {pk}")
        return Response(status=status.HTTP_204_NO_CONTENT)
