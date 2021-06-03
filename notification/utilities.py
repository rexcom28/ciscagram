from .models import Notification
from django.utils import timezone
import re

from django.contrib.auth.models import User
def create_notification(request, to_user, notification_type, objj=None):

    if notification_type in ['message', 'follower','like']:
        if notification_type=='like':
            obj = Notification.objects.create(to_user=to_user, notification_type=notification_type,created_by=request.user, post_id=objj.id)
        else:    
            notification = Notification.objects.create(to_user=to_user, notification_type=notification_type,created_by=request.user)
    elif notification_type=='comment':
        comment = Notification.objects.create(to_user=to_user, notification_type=notification_type,created_by=request.user, post_id=objj.id)
    elif notification_type == 'mcomment':
        comment = Notification.objects.create(to_user=to_user, notification_type=notification_type,created_by=request.user, post_id=objj.id)
    elif notification_type in ['update', 'mention']:
        try:
            
            obj = Notification.objects.get(to_user=to_user, notification_type=notification_type, created_by=request.user, post_id=objj.id)
            created = False
            
        except:    
            
            created = True
            obj = Notification.objects.create(to_user=to_user, notification_type=notification_type,created_by=request.user, post_id=objj.id)
            print('--Create-', 'obj: ', obj,'   created',created)

        
        if not created and obj.is_read==True:
            obj.is_read=False
            obj.notification_type='update'
            
            obj.save(force_update=True)
            print('---save---') 

def searchUser(request, instance, results, notif):
    results = re.findall("(^|[^@\w])@(\w{1,20})",instance.body)
    for result in results:
        result = result[1]
        to_user = User.objects.filter(username = result).exists()
        if to_user and result != request.user.username:
            return request, to_user, notif, instance