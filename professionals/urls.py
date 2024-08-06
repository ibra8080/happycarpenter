from django.urls import path
from . import views

urlpatterns = [
    path('advertisements/', views.AdvertisementList.as_view()),
    path('advertisements/<int:pk>/', views.AdvertisementDetail.as_view()),
    path('reviews/', views.ReviewList.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view()),
    path('job-offers/', views.JobOfferList.as_view()),
    path('job-offers/<int:pk>/', views.JobOfferDetail.as_view()),
]