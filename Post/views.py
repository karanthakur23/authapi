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
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return render(request, 'Post/user_post_view.html', {'posts': posts})


def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        caption = request.POST.get('caption')
        url = "http://127.0.0.1:8000/posts/"

        if request.user.is_authenticated:
            logged_in = request.user
            print(logged_in, 'current user')
            # Rest of your code...
        else:
            print('User is not authenticated')

        auth_token = Token.objects.get(user=logged_in)
        auth_token = auth_token.access_token
        print(auth_token, '=====================')
        payload = json.dumps({
            "caption": caption
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}',
            'Cookie': 'csrftoken=ciIyQ0eD0MQQ4ipKfFnPyhIj8jDXirDn'
        }

        print(f"Request Headers: {headers}")

        response = requests.post(url, headers=headers, data=payload)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")

    return render(request, 'Post/create_post.html', {'form': form})


def updatePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            caption = request.POST.get('caption')

            url = f"http://127.0.0.1:8000/posts/{post_id}/"

            payload = json.dumps({
            "caption": caption
            })
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0OTcyNDc4LCJpYXQiOjE3MDQ5Njg4NzgsImp0aSI6IjUzNmYzYjVlNjY1YTQzNGFiMDkxOTE4YzRkNWNiZGZmIiwidXNlcl9pZCI6MTB9.B8tKbE0jMK4dxEcuGfN3Ejc_S6w1iHdawbhgXPdHUiI',
            'Cookie': 'csrftoken=ciIyQ0eD0MQQ4ipKfFnPyhIj8jDXirDn; sessionid=kl2okh1nca7ziq0zmrzwxr0u9a9b8kg7'
            }

            response = requests.request("PUT", url, headers=headers, data=payload)
            return redirect('all-users-posts')
    return render(request, 'Post/update_post.html', {'form': form})


def deletePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':

            url = f"http://127.0.0.1:8000/posts/{post_id}/"

            payload = {}
            headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1MDM4MzE3LCJpYXQiOjE3MDUwMzQ3MTcsImp0aSI6IjRkYThkNzRlZGM3ZTQ2NTI5Yzc4MTY2N2NkYWYwZDlhIiwidXNlcl9pZCI6MTB9.Dc6kkv5m3tT793cHN-qazajBzdSqUdSiV2nVdQlUEm0',
            'Cookie': 'csrftoken=ciIyQ0eD0MQQ4ipKfFnPyhIj8jDXirDn; sessionid=kl2okh1nca7ziq0zmrzwxr0u9a9b8kg7'
            }

            response = requests.request("DELETE", url, headers=headers, data=payload)
            return redirect('all-users-posts')
    return render(request, 'Post/delete_post.html', {'post': post})


# COMMENTS ---------------------------------------------------------
# to get all comments of specific post
class PostsCommentsView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post_comments = PostComment.objects.filter(post_id=post_id)
        serializer = PostCommentSerializer(post_comments, many=True)
        return render(request, 'Post/post_comments.html', {'post_comments': post_comments})

# to comment on a post
class CommentOnPost(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def CommentOnPostView(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        comment = request.POST.get('text')
        url = f"http://127.0.0.1:8000/posts/{post_id}/comment/"

        payload = json.dumps({
        "comment_text": comment
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1MzgwNjY5LCJpYXQiOjE3MDUyOTQyNjksImp0aSI6Ijc1YTJmODllM2QyMjRjODE5ZGE5ZTRiMTM4MDI2ZTVhIiwidXNlcl9pZCI6MTV9.v5tzV6i9enbKeet_8QvD53Sdw3SraqT3W7Gtl_XRhuI',
        'Cookie': 'csrftoken=ciIyQ0eD0MQQ4ipKfFnPyhIj8jDXirDn; sessionid=kl2okh1nca7ziq0zmrzwxr0u9a9b8kg7'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
    return render(request, 'Post/comment_on_post.html', {'post': post})

# update a secific comment by id
class UpdateComment(APIView):
    # permission_classes = [IsAuthenticated]

    def put(self, request, comment_id):
        comment = get_object_or_404(PostComment, id=comment_id)
        serializer = PostCommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def updateCommentView(request, comment_id):
    comment = get_object_or_404(PostComment, id=comment_id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            comment = request.POST.get('text')

            url = f"http://127.0.0.1:8000/posts/{comment_id}/comment/update/"

            payload = json.dumps({
            "comment_text": comment
            })
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1NDAzODI5LCJpYXQiOjE3MDUzMTc0MjksImp0aSI6IjY3MzU5NjYwZWM3YjRiOGFhOTBlZTI3OGI5ZDIyZjg3IiwidXNlcl9pZCI6MTV9.XEM9IxjfbTZV3fg3D2-mrwyn_y9vjq0K13LZy57iqKI',
            'Cookie': 'csrftoken=ciIyQ0eD0MQQ4ipKfFnPyhIj8jDXirDn; sessionid=kl2okh1nca7ziq0zmrzwxr0u9a9b8kg7'
            }
            response = requests.request("PUT", url, headers=headers, data=payload)
            return redirect('all-users-posts')
    return render(request, 'Post/update_comment.html', {'comment': comment})

# delete a specific comment by id
class DeleteComment(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = get_object_or_404(PostComment, id=comment_id)
            comment.delete()
            return Response('You have deleted the comment successfully', status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response('The comment does not exist', status=status.HTTP_404_NOT_FOUND)

def deleteCommentView(request, comment_id):
    comment = get_object_or_404(PostComment, id=comment_id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':

            url = f"http://127.0.0.1:8000/posts/{comment_id}/comment/delete/"

            payload = {}
            headers = {
            'Cookie': 'csrftoken=ciIyQ0eD0MQQ4ipKfFnPyhIj8jDXirDn; sessionid=kl2okh1nca7ziq0zmrzwxr0u9a9b8kg7'
            }

            response = requests.request("DELETE", url, headers=headers, data=payload)
            return redirect('all-users-posts')
    return render(request, 'Post/delete_comment.html', {'comment': comment})

# Retrieve all comments by a specific user.
class RetrieveAllCommentsOfUser(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        comments = PostComment.objects.filter(user=user_id)
        if comments.exists():
            user_name = comments[0].user.name
        serializer = PostCommentRetrieveSerializer(comments, many=True)
        return render(request, 'Post/all_comments_of_user.html', {'comments': serializer.data, 'username': user_name})


# LIKE -----------------------------------------------------------------
#to like a post
class LikePostView(APIView):
    # permission_classes = [IsAuthenticated]

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