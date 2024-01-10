from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from .forms import PostForm
import requests
import json

# # # POSTS ----------------------------------------------
# # # to get all user's post
# class AllUsersPosts(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, post_id=None):
#         if post_id is None:
#             posts = Post.objects.all()
#             serializer = PostRetrieveSerializer(posts, many= True)
#             return Response(serializer.data)
#         else:
#             post = Post.objects.get(id=post_id)
#             serializer = PostRetrieveSerializer(post)
#             return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, post_id):
#         if post_id is not None:
#             post = get_object_or_404(Post, id=post_id)
#             serializer = PostRetrieveSerializer(post, data=request.data)

#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, post_id):
#         if post_id is not None:
#             post = get_object_or_404(Post, id=post_id)
#             post.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

# # to get all posts of specific user
# class UserPostsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, user_id):
#         user = User.objects.get(id=user_id)
#         posts = Post.objects.filter(user=user)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

# # POSTS ----------------------------------------------
# # to get all user's post
class AllUsersPosts(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, post_id=None):
        if post_id is None:
            posts = Post.objects.all()
            serializer = PostRetrieveSerializer(posts, many= True)
            return render(request, 'Post/all_users_post.html', {'posts': serializer.data})
        else:
            post = Post.objects.get(id=post_id)
            serializer = PostRetrieveSerializer(post)
            return render(request, 'Post/user_post_view.html', {'post': serializer.data})

    def post(self, request):
        # Create an instance of the serializer with no data
        serializer = PostSerializer()

        # Render the template with the empty form
        return render(request, 'Post/create_post.html', {'form': serializer})

    def put(self, request, post_id):
        if post_id is not None:
            post = get_object_or_404(Post, id=post_id)
            serializer = PostRetrieveSerializer(post, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        if post_id is not None:
            post = get_object_or_404(Post, id=post_id)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# to get all posts of specific user
class UserPostsView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        caption = request.POST.get('caption')
        url = "http://127.0.0.1:8000/posts/"

        payload = json.dumps({
        "caption": caption
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0ODgzMTMzLCJpYXQiOjE3MDQ4Nzk1MzMsImp0aSI6IjJmMDBjMGRhYzk3MzQyMDhhMDRjMjI0OTk2NDI1ZTlhIiwidXNlcl9pZCI6OX0.94ocF8iKPUYxh-7Iq1vBP9Ik9uXtnhlTFEu8BhvGfrs',
        'Cookie': 'csrftoken=ciIyQ0eD0MQQ4ipKfFnPyhIj8jDXirDn'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
    return render(request, 'Post/create_post.html', {'form': form})


def testFunc(request):
    if request.method == 'POST':
        url = "http://127.0.0.1:8000/api/user/register/"

        payload = json.dumps({
        "email": email,
        "name": name,
        "password": password,
        "password2": password2
        })
        headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=ciIyQ0eD0MQQ4ipKfFnPyhIj8jDXirDn'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
    return render(request, 'account/register.html')




























# COMMENTS ---------------------------------------------------------
# to get all comments of specific post
class PostsCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post_comments = PostComment.objects.filter(post_id=post_id)
        serializer = PostCommentSerializer(post_comments, many=True)
        return Response(serializer.data)

# to comment on a post
class CommentOnPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update a secific comment by id
class UpdateComment(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, comment_id):
        comment = get_object_or_404(PostComment, id=comment_id)
        serializer = PostCommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete a specific comment by id
class DeleteComment(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = get_object_or_404(PostComment, id=comment_id)
            comment.delete()
            return Response('You have deleted the comment successfully', status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response('The comment does not exist', status=status.HTTP_404_NOT_FOUND)

# Retrieve all comments by a specific user.
class RetrieveAllCommentsOfUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        comments = PostComment.objects.filter(user=user_id)
        serializer = PostCommentRetrieveSerializer(comments, many=True)
        return Response(serializer.data)


# LIKE -----------------------------------------------------------------
#to like a post
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if LikePost.objects.filter(user=user, post=post).exists():
            return Response('You have already liked the post', status=status.HTTP_400_BAD_REQUEST)

        like = LikePost(user=user, post=post)
        like.save()
        return Response('You have liked the post successfully', status=status.HTTP_201_CREATED)


# to unlike a post
class DislikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        like = LikePost.objects.filter(user=user, post=post).first()
        if not like:
            return Response('You have already disliked the post', status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response('You have disliked the post successfully', status=status.HTTP_204_NO_CONTENT)


# Retrieve all posts liked by a specific user.
class UserLikedPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        liked_posts = Post.objects.filter(likepost__user=user_id)
        serializer = PostRetrieveSerializer(liked_posts, many=True)
        return Response(serializer.data)








# class LikePostView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = LikePostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)