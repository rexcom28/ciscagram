from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def user_avatar_directory_path(instance, filename):
    return 'avatars/{0}/{1}'.format(instance.user.username, filename)
class Profile(models.Model):
    
    user = models.OneToOneField( User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    #avatar = models.ImageField(default='avatar.png', upload_to='avatars')
    avatar = models.ImageField(default='avatar.png', upload_to=user_avatar_directory_path)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    follows = models.ManyToManyField('self', related_name='followed_by',symmetrical=False)
    
    def __str__(self):
        return str(self.user)
    