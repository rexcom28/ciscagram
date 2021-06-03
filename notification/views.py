from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from posts.models import Post

from .models import Notification

@login_required
def notifications(request):
    goto = request.GET.get('goto', '')
    
    notification_id = request.GET.get('notification', 0)
    

    if goto != '':

        
        notification = Notification.objects.get(pk=notification_id)
    
        notification.is_read = True
        notification.save()
        
        
        


        if notification.notification_type == Notification.MESSAGE:
            return redirect('conversation:conversation', user_id=notification.created_by.id)
        
        elif notification.notification_type == Notification.FOLLOWER:
            return redirect('profiles:oinkerprofile', username=notification.created_by.username)

        elif notification.notification_type == Notification.LIKE:            
            #return redirect('profiles:oinkerprofile', username= notification.created_by.username)
            
            return redirect('posts:post-detail', pk=notification.post_id)

        elif notification.notification_type in [Notification.MENTION, Notification.UPDATE, Notification.COMMENT, Notification.MCOMMENT]:
            #return redirect('profiles:oinkerprofile', username=notification.created_by.username)  
            # (app:view, pk) 
            
            return redirect('posts:post-detail', pk=notification.post_id)

    return render(request, 'notification/notifications.html')

def error_404(request, *args, **kwargs):
        print(args,' -----------------------------------------  ',kwargs)
        return render(request,'errors/404.html',{})

def error_500(request,*args, **kwargs):
        
        return render(request,'errors/500.html', {})
        
def error_403(request, exception=None):

        return render(request,'errors/403.html')

def error_400(request,  exception=None):
        return render(request,'errors/400.html', {})