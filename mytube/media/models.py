from django.db import models
from account.models import User


class Video(models.Model):
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    thumbnail = models.URLField()
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    channel_name = models.CharField(max_length=100, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    snippet = models.CharField(max_length=300)


class Like(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
