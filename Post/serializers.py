from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComment
        fields = ['comment_text']
