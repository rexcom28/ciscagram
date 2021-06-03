from .models import Post
from profiles.models import Profile
from django.http import HttpResponse
from django.shortcuts import redirect

def action_permission(func):
    def wrapper(request,**kwargs):
        pk = kwargs.get('pk')
        new_category = request.POST.get('category')
        #print('new_category11    ',new_category)
        profile = Profile.objects.get(user=request.user)
        post = Post.objects.get(pk=pk)
        
        if profile.user.username == post.author.username:
            print('yes')
            return func(request, **kwargs)
        else:
            print('no')
            return redirect('posts:main-board')
    return wrapper