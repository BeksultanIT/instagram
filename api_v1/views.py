from api_v1.serializers.post import PostSerializer
from webapp.models import Post
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class =  PostSerializer
