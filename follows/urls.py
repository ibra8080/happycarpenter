from django.urls import path
from follows import views

urlpatterns = [
    path('follows/', views.FollowList.as_view()),
    path('follows/<int:pk>/', views.FollowDetail.as_view()),
]