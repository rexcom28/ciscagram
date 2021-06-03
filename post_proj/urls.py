
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import contact_page
from django.conf.urls import handler404,handler500,handler403,handler400

#conversation app
handler404 = 'notification.views.error_404'
handler500 = 'notification.views.error_500'
handler403 = 'notification.views.error_403'
handler400 = 'notification.views.error_400'

urlpatterns = [

    path('admin/', admin.site.urls),
    #path('contact/', include('contactforms.urls')),
    path('contact/',contact_page,name='contact_form'),
    
    path('accounts/', include('allauth.urls')),
    
    path('', include('posts.urls', namespace='posts')),
    path('', include('conversation.urls', namespace='conversation')),
    path('', include('notification.urls', namespace='notification')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
]


if settings.DEBUG: #DEV only
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)