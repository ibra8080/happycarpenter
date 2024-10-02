from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import IntegrityError
from happy_carpenter_api.permissions import IsOwnerOrReadOnly
from .models import Like
from .serializers import LikeSerializer

class LikeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except IntegrityError:
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

class LikeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.filter(
            owner=self.request.user,
            post__id=self.kwargs['pk']
        ).first()
        if not obj:
            return Response(
                {"detail": "Like not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(self.request, obj)
        return obj
