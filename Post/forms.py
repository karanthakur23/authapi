from django import forms
from .models import Post, LikePost, PostComment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['comment_text']