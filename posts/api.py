import json
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from notification.utilities import create_notification
from posts.models import *
from django.contrib.auth.models import User
import re


@login_required
def api_categoryAddPost(request):
    pass