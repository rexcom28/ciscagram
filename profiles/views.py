from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def my_profile_view(request):
    obj = Profile.objects.get(user= request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=obj)
    #print('request.is_ajax() ', request.is_ajax())
    if request.is_ajax():
        if form.is_valid():
            instance = form.save()
            return JsonResponse({
                'bio': instance.bio,
                'avatar': instance.avatar.url,
                'user': instance.user.username
            })
    context = {
        'obj':obj,
        'form': form,
    }
    return render(request, 'profiles/main.html', context)

def oinkerprofile(request, username=None):
    print('-----------------------USER',username)
    #user = get_object_or_404(User, username=username)
    user = User.objects.get(username=username)
    posts= user.posts.all()
    print('oinkerprofile  ', user,'   ',posts)
    context ={
        'u':user,
        'posts':posts
    }
    return render(request, 'profiles/oinkerprofile.html', context)

@login_required
def follow_oinker(request, username):
    user = User.objects.get(username= username)
    print('follow_oinker',user.profile.id)
    request.user.profile.follows.add(user.profile)
    return redirect('profiles:oinkerprofile' , username=user.username)
    
@login_required
def unfollow_oinker(request, username):
    user =User.objects.get(username=username)
    print('unfollow_oinker  ', user)
    request.user.profile.follows.remove(user.profile)
    return redirect('profiles:oinkerprofile' , username=user.username)