from django import forms
from .models import Image, Licence


class ImageForm(forms.ModelForm):
    licence = forms.ModelChoiceField(queryset=Licence.objects.all())
    
    class Meta:
        model = Image
        fields = ['name', 'auteur', 'image', 'payment_required', 'price', 'description', 'tags']
        