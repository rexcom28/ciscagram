from django.urls import path
from .views import *

app_name = 'notification'

urlpatterns = [
    path('notifications/', notifications, name='notifications'),

]

