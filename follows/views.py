from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Follow
from .serializers import FollowSerializer

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
    queryset = Follow.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {
            'owner': self.request.user,
            'followed__username': self.kwargs['pk']
        }
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
