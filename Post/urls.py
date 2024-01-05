from django.urls import path
from Post.views import *

urlpatterns = [
    path('', AllUsersPosts.as_view()),
    path('user/<int:user_id>/', UserPostsView.as_view()),
    path('comments/<int:post_id>/', PostsCommentsView.as_view()),
    path('<int:post_id>/comment/', CommentOnPost.as_view(), name='comment-on-post'),
]