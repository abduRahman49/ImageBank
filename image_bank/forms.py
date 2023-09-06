from allauth.account.forms import SignupForm
from django import forms
from .models import Image, Licence, CustomUser
from django.core import validators
from taggit.forms import TagWidget


class ImageForm(forms.ModelForm):
    licence = forms.ModelChoiceField(queryset=Licence.objects.only('name'))
    auteur = forms.ModelChoiceField(queryset=CustomUser.objects.only('username'))
    
    class Meta:
        model = Image
        fields = ['name', 'auteur', 'image', 'payment_required', 'price', 'description', 'tags']
        
        widgets = {
            'tags': TagWidget(attrs={'class': 'form-control'}),
        }


# class AppSignupForm(SignupForm):
#     def save(self, request):

#         # Ensure you call the parent class's save.
#         # .save() returns a User object.
#         user = super(AppSignupForm, self).save(request)

#         # Add your own processing here.

#         # You must return the original result.
#         return user

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