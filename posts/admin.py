from django.contrib import admin
from .models import Post, Doc, Category
# Register your models here.
admin.site.register(Post)
admin.site.register(Doc)
admin.site.register(Category)