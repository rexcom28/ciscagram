from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name='conversations')
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)


    class Meta:
        ordering = ['created_at']
    
    def save(self, *args, **kwargs):
        self.conversation.save()

        super(ConversationMessage, self).save(*args, **kwargs)

class postMessage(models.Model):
    message_post_id = models.ForeignKey(Post, related_name='messeges_posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='messeges_posts', on_delete=models.CASCADE)
    class Meta:
        ordering = ['created_at']