from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from .forms import PostForm, CommentForm
import requests
import json
from account.models import *
from django.contrib.auth.decorators import login_required

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
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id=None):
        logged_in = request.user
        print(logged_in, 'currentuser==')
        form= PostForm()
        if post_id is None:
            posts = Post.objects.all()
            serializer = PostRetrieveSerializer(posts, many= True)
            return render(request, 'Post/all_users_post.html', {'posts': serializer.data, 'form': form})
        else:
            post = Post.objects.get(id=post_id)
            serializer = PostRetrieveSerializer(post)
            return render(request, 'Post/user_post_view.html', {'post': serializer.data})

    def post(self, request):
        print(request.user, "create post logged in user")
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_id):
        if post_id is not None:
            post = get_object_or_404(Post, id=post_id)
            serializer = PostSerializer(post, data=request.data)

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
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def UserPosts(request, user_id):
    user = User.objects.get(id=user_id)
    token = Token.objects.get(user=user)
    token_access = token.access_token
    return render(request, 'Post/user_post_view.html', {'user_id': user_id, 'token_access': token_access})


def createPost(request):
    form = PostForm()
    user = request.user
    print(user, 'user-+')
    return render(request, 'Post/create_post.html', {'form': form})


def updatePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_caption = post.caption
    user = post.user
    token = Token.objects.get(user=user)
    token_access = token.access_token
    return render(request, 'Post/update_post.html', {'post_caption': post_caption, 'token_access': token_access, 'post_id': post_id})


def deletePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = post.user
    token = Token.objects.get(user=user)
    token_access = token.access_token
    print(token_access, 'token')
    return render(request, 'Post/delete_post.html', {'post': post, 'token_access': token_access, 'post_id': post_id})


# COMMENTS ---------------------------------------------------------
# to get all comments of specific post
# class PostsCommentsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, post_id):
#         post_comments = PostComment.objects.filter(post_id=post_id)
#         serializer = PostCommentSerializer(post_comments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

def postsComments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # user = post.user
    # token = Token.objects.get(user=user)
    # token_access = token.access_token
    post_comments = PostComment.objects.filter(post_id=post_id)
    serializer = PostCommentSerializer(post_comments, many=True)
    return render(request, 'Post/post_comments.html', {'post_comments': post_comments, 'post_id': post_id})

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

def CommentOnPostView(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = post.user
    token = Token.objects.get(user=user)
    token_access = token.access_token
    return render(request, 'Post/comment_on_post.html', {'post': post, 'token_access': token_access, 'post_id': post_id})

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

def updateCommentView(request, comment_id):
    comment = get_object_or_404(PostComment, id=comment_id)
    text = comment.comment_text
    user = comment.user
    token = Token.objects.get(user=user)
    token_access = token.access_token
    return render(request, 'Post/update_comment.html', {'text': text, 'token_access': token_access, 'comment_id': comment_id})

# delete a specific comment by id
class DeleteComment(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = get_object_or_404(PostComment, id=comment_id)
            comment.delete()
            return Response({'message': 'You have deleted the comment successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'message': 'The comment does not exist'}, status=status.HTTP_404_NOT_FOUND)

def deleteCommentView(request, comment_id):
    comment = get_object_or_404(PostComment, id=comment_id)
    user = comment.user
    token = Token.objects.get(user=user)
    access_token = token.access_token
    return render(request, 'Post/delete_comment.html', {'comment': comment, 'access_token': access_token, 'comment_id': comment_id})

# Retrieve all comments by a specific user.
class RetrieveAllCommentsOfUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        comments = PostComment.objects.filter(user=user_id)
        serializer = PostCommentRetrieveSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def allUsersComment(request, user_id):
    comments = PostComment.objects.filter(user=user_id)
    if comments.exists():
        user_name = comments[0].user.id
    token = Token.objects.get(user=user_name)
    access_token = token.access_token
    return render(request, 'Post/all_comments_of_user.html', {'comments': comments, 'username': user_name})

# LIKE -----------------------------------------------------------------
#to like a post
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        print(post, 'post----------------')
        print(user, 'user----------------')
        if LikePost.objects.filter(user=user, post=post).exists():
            return Response('You have already liked the post', status=status.HTTP_400_BAD_REQUEST)

        like = LikePost(user=user, post=post)
        like.save()
        return Response('You have liked the post successfully', status=status.HTTP_201_CREATED)


# to unlike a post
class DislikePostView(APIView):
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]

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