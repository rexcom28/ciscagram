from django import forms
from django.forms import fields

#from posts.views import category
from .models import Post, Category
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    # title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # body  = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':3}))
    class Meta:
        model = Post
        fields = ('title', 'body','category','visible')
        labels = {
            'visible': _('Uncheck if NSFW'),
        }
class PostCategoryForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'body', 'category','visible')
        labels = {
            'visible': _('Uncheck if NSFW'),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model =Category
        fields= ('title', 'description','upload','NSFWs')
        labels = {
            'NSFWs': _('Check if NSFW'),
        }
