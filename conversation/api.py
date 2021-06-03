import json
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from notification.utilities import create_notification

from .models import ConversationMessage, postMessage
from posts.models import Post
from django.contrib.auth.models import User
import re
@login_required
def api_add_message(request):
    data = json.loads(request.body)
    
    content = data['content']
    conversation_id = data['conversation_id']
    
    message = ConversationMessage.objects.create(conversation_id=conversation_id, content=content, created_by=request.user)

    for user in message.conversation.users.all():
        if user != request.user:
            create_notification(request, user, 'message')
            #print(request, user, 'message-----------------------')

    return JsonResponse({'success':True})

@login_required
def api_add_message_post(request):
    data = json.loads(request.body)

    content = data['content']
    message_post_id = data['post_id']
    
    post=Post.objects.get(pk=message_post_id)
    postM = postMessage.objects.create(message_post_id=post, content=content, created_by=request.user)
    postMM = postMessage.objects.filter(id=postM.pk)
    res = None
    data=[]
    for message in postMM:
        print(message)
        item={
            'id':message.id,
            'author': message.created_by.username
        }
        data.append(item)
    res=data
    
    
    
    
    content = re.findall("(^|[^@\w])@(\w{1,20})",postM.content)
    for result in content:
        result = result[1]
        c = User.objects.filter(username = result).exists()
        #print("SOOL   " ,result, '     c: ',c , 'request.user.username: ',request.user.username) 
        if c and result != request.user.username:
            create_notification(request, User.objects.get(username=result) , 'mcomment', post)    
    #print('Post Author: ',post.author,'  logginUser',request.user)

    if post.author !=request.user :
        
        to_user = User.objects.get(username=post.author) 

        create_notification(request, to_user , 'comment', post)

    return JsonResponse({'data':res})