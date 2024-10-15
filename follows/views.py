from rest_framework import generics, permissions
from happy_carpenter_api.permissions import IsOwnerOrReadOnly
from .models import Follow
from .serializers import FollowSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User

class FollowList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        followed_id = self.request.data.get('followed')
        try:
            followed_user = User.objects.get(id=followed_id)
            serializer.save(owner=self.request.user, followed=followed_user)
        except User.DoesNotExist:
            raise serializers.ValidationError("User to follow does not exist.")

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FollowDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {
            'owner': self.request.user,
            'followed__id': self.kwargs['pk']
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
