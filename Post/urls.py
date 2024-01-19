from django.urls import path
from Post.views import *

urlpatterns = [
    path('', AllUsersPosts.as_view(), name='all-users-posts'),
    path('create_post/', AllUsersPosts.as_view()),
    path('<int:post_id>/', AllUsersPosts.as_view()),
    path('user/<int:user_id>/', UserPostsView.as_view()),

    # path('comments/<int:post_id>/', PostsCommentsView.as_view()),
    path('<int:post_id>/comment/', CommentOnPost.as_view(), name='comment-on-post'),
    path('<int:comment_id>/comment/delete/', DeleteComment.as_view()),
    path('<int:comment_id>/comment/update/', UpdateComment.as_view(), name='update-on-post'),
    path('user/<int:user_id>/comments/', RetrieveAllCommentsOfUser.as_view(), name='users-comment'),

    path('<int:post_id>/like/', LikePostView.as_view(), name='like-on-post'),
    path('<int:post_id>/dislike/', DislikePostView.as_view(), name='dislike-on-post'),
    path('<int:user_id>/liked-posts/', UserLikedPosts.as_view(), name='liked-posts'),

    # django function based
    path('create-post/', createPost, name='create-post'),
    path('update-post/<int:post_id>/', updatePost, name='update-post'),
    path('delete-post/<int:post_id>/', deletePost, name='delete-post'),
    path('comment-on-post/<int:post_id>/', CommentOnPostView, name='comment-on-post-view'),
    path('comment-update/<int:comment_id>/', updateCommentView, name='comment-update'),
    path('comment-delete/<int:comment_id>/', deleteCommentView, name='comment-delete'),

    path('user-posts/<int:user_id>/', UserPosts, name='user-posts'),
    path('users-comment/<int:user_id>/', allUsersComment),
    path('post-comments/<int:post_id>/', postsComments),
]