from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        labels = {
            'image' : 'Choose Picture Profile:', 
        }

        attrs_input = {
            'class' : 'form-control form-control-sm',
        }

        widgets = {
            'image': forms.FileInput(
                attrs = attrs_input,
            ),
          
        }