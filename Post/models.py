from django.db import models
from account.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField()
    # image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"Post by {self.user.name} at {self.uploaded_at}"

class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)

    class Meta:
        unique_together = (('post', 'user'),)

class PostComment(models.Model):
    comment_text = models.CharField(max_length= 300)
    created_at = models.DateTimeField(auto_now_add= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.name} - {self.comment_text}"