from rest_framework import serializers
from webapp.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','image', 'content', 'author']
        read_only_fields = ['id']