
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#conversation app
from .views import conversations, conversation
from .api import api_add_message, api_add_message_post
app_name = 'conversation'
urlpatterns = [
    path('conversations/', conversations, name='conversation-s'),
    path('conversations/<int:user_id>/', conversation, name='conversation'),
    path('api/add_message/', api_add_message, name='api_add_message'),
    path('api/add_message_post/', api_add_message_post, name='api_add_message_post'),

]

