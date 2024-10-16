from rest_framework import generics, permissions, status
from rest_framework.response import Response
from happy_carpenter_api.permissions import IsOwnerOrReadOnly
from .models import Follow
from .serializers import FollowSerializer

class FollowList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FollowDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {
            'owner': self.request.user,
            'followed__id': self.kwargs['pk']
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"detail": "Follow relationship not found."}, status=status.HTTP_404_NOT_FOUND)
