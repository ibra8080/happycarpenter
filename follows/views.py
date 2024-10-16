from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Follow
from .serializers import FollowSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class FollowList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = Follow.objects.all()
        followed = self.request.query_params.get('followed')
        owner = self.request.query_params.get('owner')
        
        if followed:
            queryset = queryset.filter(followed__username=followed)
        if owner:
            queryset = queryset.filter(owner__username=owner)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FollowDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def get_object(self):
        followed_username = self.kwargs['pk']
        followed_user = get_object_or_404(User, username=followed_username)
        return Follow.objects.filter(owner=self.request.user, followed=followed_user).first()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Already unfollowed."}, status=status.HTTP_200_OK)
