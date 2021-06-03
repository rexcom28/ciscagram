from django.urls import path
from .views import my_profile_view, oinkerprofile, follow_oinker, unfollow_oinker
app_name = 'profiles'

urlpatterns = [
    path('my/', my_profile_view, name='my-profile'),
    path('u/<str:username>/', oinkerprofile, name='oinkerprofile'),
    path('u/<str:username>/follow/', follow_oinker, name='follow-oinker'),
    path('u/<str:username>/unfollow/', unfollow_oinker, name='unfollow-oinker'),
]