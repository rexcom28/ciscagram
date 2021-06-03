from django.contrib import admin
from .models import Conversation, ConversationMessage, postMessage
# Register your models here.
admin.site.register(Conversation)
admin.site.register(ConversationMessage)
admin.site.register(postMessage)