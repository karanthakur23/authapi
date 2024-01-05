from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.

# to get all user's post
class AllUsersPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many= True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# to get all posts of specific user
class UserPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# to get all comments of specific post
class PostsCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post_comments = PostComment.objects.filter(post_id=post_id)
        serializer = PostCommentSerializer(post_comments, many=True)
        return Response(serializer.data)

# to comment on a post
class CommentOnPost(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


















# class LikePostView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = LikePostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)