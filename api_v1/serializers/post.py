from rest_framework import serializers
from webapp.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'image', 'image_url', 'content', 'author', 'likes_count', 'is_liked']
        read_only_fields = ['id', 'author', 'likes_count', 'is_liked']

    def get_image_url(self, obj):
        request = self.context.get('request')
        try:
            url = obj.image.url
        except Exception:
            return None
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    def get_is_liked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None) if request else None
        if user and user.is_authenticated:
            return obj.like_users.filter(pk=user.pk).exists()
        return False
