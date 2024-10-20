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
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Advertisement.objects.all().order_by('-created_at')
        if self.request.method == 'GET':
            professional_id = self.request.query_params.get('professional')
            if professional_id:
                queryset = queryset.filter(professional__id=professional_id)
        return queryset

    def list(self, request, *args, **kwargs):
        logger.info(f"Listing advertisements. User: {request.user}, Params: {request.query_params}")
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing advertisements: {str(e)}")
            return Response({"detail": "An error occurred while fetching advertisements."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating advertisement. User: {request.user}")
        if request.user.profile.user_type != 'professional':
            return Response({"detail": "Only professional users can create advertisements."}, status=status.HTTP_403_FORBIDDEN)
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info(f"Advertisement created successfully. Data: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating advertisement: {str(e)}", exc_info=True)
            return Response({"detail": f"An error occurred while creating the advertisement: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        logger.info(f"Performing create for user: {self.request.user}")
        serializer.save(professional=self.request.user, owner=self.request.user)

class AdvertisementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Advertisement.objects.filter(professional=user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            logger.info(f"Attempting to delete advertisement {instance.id} by user {request.user}")
            self.perform_destroy(instance)
            logger.info(f"Advertisement {instance.id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting advertisement: {str(e)}", exc_info=True)
            return Response({"detail": f"Failed to delete advertisement: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        logger.info(f"Updating advertisement {instance.id} for user {request.user}")
        logger.info(f"Request data: {request.data}")
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            logger.info(f"Serializer validated data: {serializer.validated_data}")
            self.perform_update(serializer)
            logger.info(f"Advertisement {instance.id} updated successfully")
            return Response(serializer.data)
        except serializers.ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating advertisement: {str(e)}", exc_info=True)
            return Response({"detail": f"An error occurred while updating the advertisement: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_update(self, serializer):
        serializer.save()


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        professional_username = self.request.query_params.get('professional')
        logger.info(f"Fetching reviews for professional: {professional_username}")
        if professional_username:
            queryset = Review.objects.filter(professional__username=professional_username)
            logger.info(f"Found {queryset.count()} reviews for {professional_username}")
            return queryset
        logger.info("Fetching all reviews")
        return Review.objects.all()

    def perform_create(self, serializer):
        professional_username = self.request.data.get('professional')
        logger.info(f"Creating review for professional: {professional_username}")
        try:
            professional = User.objects.get(username=professional_username)
            serializer.save(owner=self.request.user, professional=professional)
            logger.info(f"Review created successfully for {professional_username}")
        except User.DoesNotExist:
            logger.error(f"Professional user {professional_username} not found")
            raise serializers.ValidationError("Professional user not found")

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            logger.info(f"Attempting to delete review {instance.id} by user {request.user}")
            self.perform_destroy(instance)
            logger.info(f"Review {instance.id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting review: {str(e)}", exc_info=True)
            return Response({"detail": f"Failed to delete review: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobOfferList(generics.ListCreateAPIView):
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get('role', 'auto')
        logger.info(f"Getting job offers for user: {user.username}, user type: {user.profile.user_type}, role: {role}")
        
        if role == 'professional' or (role == 'auto' and user.profile.user_type == 'professional'):
            queryset = JobOffer.objects.filter(professional=user)
            logger.info(f"Professional view, found {queryset.count()} job offers")
        else:
            queryset = JobOffer.objects.filter(client=user)
            logger.info(f"Client view, found {queryset.count()} job offers")
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
        logger.info(f"Creating job offer. User: {request.user}, Data: {request.data}")

        professional_id = request.data.get('professional')
        ad_id = request.data.get('advertisement')
        
        if not professional_id or not ad_id:
            return Response({"detail": "Both professional and advertisement IDs are required."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            professional = User.objects.get(id=professional_id)
            advertisement = Advertisement.objects.get(id=ad_id)
        except User.DoesNotExist:
            return Response({"detail": "Invalid professional ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Advertisement.DoesNotExist:
            return Response({"detail": "Invalid advertisement ID"}, status=status.HTTP_400_BAD_REQUEST)

        if professional.profile.user_type != 'professional':
            return Response({"detail": "The selected user is not a professional."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        job_offer = serializer.save(
            client=request.user,
            professional=professional,
            advertisement=advertisement
        )

        headers = self.get_success_headers(serializer.data)
        logger.info(f"Job offer created successfully. ID: {job_offer.id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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