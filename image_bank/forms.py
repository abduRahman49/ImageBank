from django import forms
from .models import Image, Licence, ImageBankUser
from django.core import validators
from taggit.forms import TagWidget


class ImageForm(forms.ModelForm):
    licence = forms.ModelChoiceField(queryset=Licence.objects.all())
    auteur = forms.ModelChoiceField(queryset=ImageBankUser.objects.all())
    
    class Meta:
        model = Image
        fields = ['name', 'auteur', 'image', 'payment_required', 'price', 'description', 'new_tags']
        
        widgets = {
            'new_tags': TagWidget(attrs={'class': 'form-control tag-input'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['new_tags'].required = False
        self.fields['licence'].required = False


class NewUserForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control', 'aria-label': 'Username'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'aria-label': 'Email'})
    )
    password = forms.CharField(
        label='Password',
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'aria-label': 'Password'})
    )
    

class RegisteredUserForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'aria-label': 'Email'})
    )
    password = forms.CharField(
        label='Password',
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'aria-label': 'Password'})
    )
    

class UploadPictureForm(forms.ModelForm):
    
    class Meta:
        model = ImageBankUser
        fields = ['profile_pic']