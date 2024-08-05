from rest_framework import generics, permissions
from happy_carpenter_api.permissions import IsOwnerOrReadOnly
from .models import Follow
from .serializers import FollowSerializer

class FollowList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FollowDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer