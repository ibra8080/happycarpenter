from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Post, Comment, Category  
from .serializers import PostSerializer, CommentSerializer, CategorySerializer  
from happy_carpenter_api.permissions import IsOwnerOrReadOnly
import logging

logger = logging.getLogger(__name__)


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['categories', 'owner__profile__user_type', 'image_filter']
    # search_fields = ['title', 'content', 'owner__username', 'categories__name']
    # ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def list(self, request, *args, **kwargs):
        logger.error("Entering PostList view")
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in PostList view: {str(e)}")
            raise

    def perform_create(self, serializer):
        logger.error("Attempting to create post")
        try:
            serializer.save(owner=self.request.user)
        except Exception as e:
            logger.error(f"Error creating post: {str(e)}")
            raise

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PostDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
