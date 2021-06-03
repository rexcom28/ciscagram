
from .models import Profile
from . models import * 
from django import  forms

class ProfileForm(forms.ModelForm):
    birthdate = forms.DateField()
    class Meta:
        model = Profile
        fields = ('bio', 'avatar', 'birthdate',)

