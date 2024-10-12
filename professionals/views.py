from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Advertisement, Review, JobOffer
from .serializers import AdvertisementSerializer, ReviewSerializer, JobOfferSerializer
from profiles.models import Profile
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
import logging
import traceback
from django.utils import timezone
from rest_framework.filters import OrderingFilter
from happy_carpenter_api.permissions import IsOwnerOrReadOnly

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
        if request.user.profile.user_type != 'professional':
            return Response({"detail": "Only professional users can create advertisements."}, status=status.HTTP_403_FORBIDDEN)
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
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(professional__profile__user_type='professional')

    def perform_create(self, serializer):
        professional = User.objects.get(id=self.request.data.get('professional'))
        if professional.profile.user_type != 'professional':
            raise serializers.ValidationError("The user is not a professional.")
        serializer.save(reviewer=self.request.user, professional=professional)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class JobOfferList(generics.ListCreateAPIView):
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        logger.info(f"Getting job offers for user: {user.username}, user type: {user.profile.user_type}")
        if user.profile.user_type == 'professional':
            queryset = JobOffer.objects.filter(professional=user)
            logger.info(f"Professional user, found {queryset.count()} job offers")
        else:
            queryset = JobOffer.objects.filter(client=user)
            logger.info(f"Client user, found {queryset.count()} job offers")
        return queryset

    def list(self, request, *args, **kwargs):
        logger.info(f"Listing job offers for user: {request.user}")
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            logger.info(f"Returning {len(serializer.data)} job offers")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing job offers: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({"detail": "An error occurred while fetching job offers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating job offer. User: {request.user}")
        try:
            professional_id = request.data.get('professional')
            advertisement_id = request.data.get('advertisement')
            
            professional = User.objects.get(id=professional_id)
            advertisement = Advertisement.objects.get(id=advertisement_id)
            
            if professional.profile.user_type != 'professional':
                raise serializers.ValidationError("The selected user is not a professional.")
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(client=request.user)
            
            headers = self.get_success_headers(serializer.data)
            logger.info(f"Job offer created successfully. Data: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except User.DoesNotExist:
            return Response({"detail": "Invalid professional ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Advertisement.DoesNotExist:
            return Response({"detail": "Invalid advertisement ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating job offer: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class JobOfferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

class JobOfferCreate(generics.CreateAPIView):
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        professional_id = self.kwargs.get('professional_id')
        ad_id = self.kwargs.get('ad_id')
        
        logger.info(f"Creating job offer. User: {request.user}, Professional ID: {professional_id}, Ad ID: {ad_id}")
        
        try:
            professional = User.objects.get(id=professional_id)
            advertisement = Advertisement.objects.get(id=ad_id)
            
            if professional.profile.user_type != 'professional':
                raise serializers.ValidationError("The selected user is not a professional.")
            
            data = request.data.copy()
            data['professional'] = professional_id
            data['advertisement'] = ad_id
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(client=request.user)
            
            headers = self.get_success_headers(serializer.data)
            logger.info(f"Job offer created successfully. Data: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except User.DoesNotExist:
            return Response({"detail": "Invalid professional ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Advertisement.DoesNotExist:
            return Response({"detail": "Invalid advertisement ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating job offer: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_job_offer_status(request, offer_id):
    logger.info(f"Attempting to update job offer {offer_id} for user {request.user}")
    try:
        job_offer = JobOffer.objects.get(id=offer_id, professional=request.user)
    except JobOffer.DoesNotExist:
        logger.error(f"Job offer {offer_id} not found for user {request.user}")
        return Response({"detail": "Job offer not found."}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    feedback = request.data.get('feedback', '')

    logger.info(f"Updating job offer {offer_id} to status: {new_status}")

    if new_status not in dict(JobOffer.STATUS_CHOICES).keys():
        logger.error(f"Invalid status {new_status} for job offer {offer_id}")
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        job_offer.status = new_status
        job_offer.feedback = feedback
        job_offer.status_updated_at = timezone.now()
        job_offer.save()
        logger.info(f"Successfully updated job offer {offer_id} to status {new_status}")
    except Exception as e:
        logger.error(f"Error saving job offer {offer_id}: {str(e)}")
        return Response({"detail": f"Error updating job offer: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = JobOfferSerializer(job_offer)
    return Response(serializer.data)