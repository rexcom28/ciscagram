from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'images/{0}/{1}/{2}'.format(instance.photo_id.author.username, instance.photo_id.id, filename)

def user_category_path(instance,filename):
    return 'images/{0}/{1}/{2}'.format(instance.created_by.username, instance.title, filename)

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upload = models.ImageField(upload_to=user_category_path, blank=True, null=True)
    #upload = models.ImageField(upload_to='images/', blank=True, null=True)
    NSFWs = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    liked = models.ManyToManyField(User, blank=True)
    #author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.title)

    @property
    def like_count(self):
        return self.liked.all().count()
    def get_photos(self):
        return self.photo_set.all()

    class Meta:
        ordering = ("-created",)


class Doc(models.Model):
    photo_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photo_set')
    upload = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return str(self.pk)
    

