from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from api_v1.serializers.post import PostSerializer
from api_v1.permissions import IsAuthorOrReadOnly
from webapp.models import Post


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('like_users')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        post.like_users.add(request.user)
        return Response({'liked': True, 'likes_count': post.like_users.count()})

    @like.mapping.delete
    def unlike(self, request, pk=None):
        post = self.get_object()
        post.like_users.remove(request.user)
        return Response({'liked': False, 'likes_count': post.like_users.count()})
