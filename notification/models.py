from django.db import models
from posts.models import Post
from django.contrib.auth.models import User

class Notification(models.Model):
    MESSAGE = 'message'
    FOLLOWER = 'follower'
    LIKE = 'like'
    MENTION = 'mention'
    UPDATE  = 'update'
    COMMENT = 'comment'
    MCOMMENT = 'mcomment'
    CHOICES = (
        (MESSAGE, 'Message'),
        (FOLLOWER, 'Follower'),
        (LIKE, 'Like'),
        (MENTION, 'Mention'),
        (UPDATE, 'Update'),
        (COMMENT, 'comment'),
        (MCOMMENT, 'mcomment'),
    )

    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)

    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='creatednotifications', on_delete=models.CASCADE)
    post_id     = models.IntegerField(blank=True, null=True)
    class Meta:
        ordering = ['-created_at']