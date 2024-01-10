from rest_framework import serializers
from .models import *

# POST
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['caption']

class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'caption', 'uploaded_at']

# LIKE
class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'

# COMMENT
class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['comment_text']

class PostCommentRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['comment_text', 'user', 'post', 'created_at']