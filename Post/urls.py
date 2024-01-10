from django.urls import path
from Post.views import *

urlpatterns = [
    path('', AllUsersPosts.as_view()),
    path('create_post/', AllUsersPosts.as_view()),
    path('<int:post_id>/', AllUsersPosts.as_view()),
    path('user/<int:user_id>/', UserPostsView.as_view()),

    path('comments/<int:post_id>/', PostsCommentsView.as_view()),
    path('<int:post_id>/comment/', CommentOnPost.as_view(), name='comment-on-post'),
    path('<int:comment_id>/comment/delete/', DeleteComment.as_view()),
    path('<int:comment_id>/comment/update/', UpdateComment.as_view(), name='update-on-post'),
    path('user/<int:user_id>/comments/', RetrieveAllCommentsOfUser.as_view(), name='users-comment'),

    path('<int:post_id>/like/', LikePostView.as_view(), name='like-on-post'),
    path('<int:post_id>/dislike/', DislikePostView.as_view(), name='dislike-on-post'),
    path('<int:user_id>/liked-posts/', UserLikedPosts.as_view(), name='liked-posts'),

    # django function based
    path('create-post/', createPost, name='create-post'),
]