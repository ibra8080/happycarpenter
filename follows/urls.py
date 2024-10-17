from django.urls import path
from . import views

urlpatterns = [
    path('follows/', views.FollowList.as_view(), name='follow-list'),
    path('follows/<str:pk>/', views.FollowDetail.as_view(), name='follow-detail'),
]
