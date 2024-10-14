from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import transaction
from .models import Post, Comment, Category
from .serializers import PostSerializer, CommentSerializer, CategorySerializer
from happy_carpenter_api.permissions import IsOwnerOrReadOnly
import logging


logger = logging.getLogger(__name__)


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'categories', 'owner__profile__user_type', 'image_filter']
    search_fields = ['title', 'content', 'owner__username', 'categories__name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = '-created_at'

    def create(self, request, *args, **kwargs):
        logger.info(f"Received POST request. Data: {request.data}")
        logger.info(f"Files: {request.FILES}")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            logger.info("Serializer is valid")
            try:
                with transaction.atomic():
                    post = self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                logger.info(
                        f"Post created successfully. Data: {serializer.data}")
                return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)
            except Exception as e:
                logger.error(f"Error creating post: {str(e)}")
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        logger.info("Performing create")
        post = serializer.save(owner=self.request.user)
        logger.info(f"Post saved with ID: {post.id}")
        return post


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
            try:
                with transaction.atomic():
                    serializer.save()
                logger.info(f"Post {pk} updated successfully")
                return Response(serializer.data)
            except Exception as e:
                logger.error(f"Error updating post {pk}: {str(e)}")
                return Response(
                        {"error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.error(f"Error updating post {pk}: {serializer.errors}")
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        post = self.get_object(pk)
        try:
            post.delete()
            logger.info(f"Post {pk} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting post {pk}: {str(e)}")
            return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        return Comment.objects.filter(post__id=post_id) if post_id else Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
