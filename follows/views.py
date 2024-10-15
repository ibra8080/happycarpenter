from rest_framework import generics, permissions
from happy_carpenter_api.permissions import IsOwnerOrReadOnly
from .models import Follow
from .serializers import FollowSerializer


class FollowList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        followed_username = self.request.data.get('followed')
        followed_user = User.objects.get(username=followed_username)
        serializer.save(owner=self.request.user, followed=followed_user)


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
