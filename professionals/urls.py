from django.urls import path
from . import views

urlpatterns = [
    path('advertisements/', views.AdvertisementList.as_view()),
    path('advertisements/<int:pk>/', views.AdvertisementDetail.as_view()),
    path('reviews/', views.ReviewList.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view()),
    path('job-offers/', views.JobOfferList.as_view()),
    path('job-offers/<int:pk>/', views.JobOfferDetail.as_view()),
    path('job-offers/create/', views.JobOfferCreate.as_view(), name='job-offer-create'),
    path('job-offers/<int:offer_id>/update-status/', views.update_job_offer_status, name='update-job-offer-status'),
]