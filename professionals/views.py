from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Advertisement, Review, JobOffer
from .serializers import AdvertisementSerializer, ReviewSerializer, JobOfferSerializer
from profiles.models import Profile
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
import logging
import traceback

logger = logging.getLogger(__name__)

class IsProfessionalUser(permissions.BasePermission):
    def has_permission(self, request, view):
        logger.info(f"Checking IsProfessionalUser for user: {request.user}")
        is_professional = request.user.is_authenticated and request.user.profile.user_type == 'professional'
        logger.info(f"User is professional: {is_professional}")
        return is_professional

class IsProfessionalOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        logger.info(f"Checking IsProfessionalOrReadOnly for user: {request.user}, method: {request.method}")
        if request.method in permissions.SAFE_METHODS:
            logger.info("Safe method, granting permission")
            return True
        is_professional = request.user.is_authenticated and request.user.profile.user_type == 'professional'
        logger.info(f"User is professional: {is_professional}")
        return is_professional

class AdvertisementList(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsProfessionalOrReadOnly]

    def list(self, request, *args, **kwargs):
        logger.info(f"Listing advertisements. User: {request.user}")
        try:
            logger.info("Fetching queryset")
            queryset = self.filter_queryset(self.get_queryset())
            logger.info(f"Queryset count: {queryset.count()}")

            logger.info("Paginating queryset")
            page = self.paginate_queryset(queryset)
            if page is not None:
                logger.info("Serializing paginated data")
                serializer = self.get_serializer(page, many=True)
                logger.info("Returning paginated response")
                return self.get_paginated_response(serializer.data)

            logger.info("Serializing full queryset")
            serializer = self.get_serializer(queryset, many=True)
            logger.info("Returning full response")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing advertisements: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({"detail": "An error occurred while fetching advertisements."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating advertisement. User: {request.user}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating advertisement: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({"detail": "An error occurred while creating the advertisement."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        logger.info(f"Performing create for user: {self.request.user}")
        serializer.save(professional=self.request.user)

class AdvertisementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsProfessionalOrReadOnly]

class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['professional']

    def perform_create(self, serializer):
        professional_id = self.request.data.get('professional')
        try:
            professional = User.objects.get(id=professional_id)
            if professional.profile.user_type != 'professional':
                raise serializers.ValidationError(
                        {"professional": "The user is not a professional."})
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"professional": "Professional not found."})

        serializer.save(reviewer=self.request.user, professional=professional)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class JobOfferList(generics.ListCreateAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class JobOfferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.IsAuthenticated]
