import json
from PIL import Image as PImage
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ImageForm, NewUserForm, RegisteredUserForm
from .models import Licence, Tag, CustomUser, Image
from api.serializers import ImageSerializer, CustomUserSerializer
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator


# Create your views here.
@login_required
def index(request):
    form = ImageForm()
    return render(request, 'image_bank/index.html', {'form': form})

def signup_contributeur(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = CustomUser.objects.create_user(data.get('username'), data.get('email'), data.get('password'))
                user.role = "C"
                user.save()
                return redirect(reverse('sign-in-contributeur'))
            except IntegrityError:
                messages.add_message(request, messages.constants.ERROR, 'Utilisateur déjà existant')
                return redirect(reverse('sign-up-contributeur'))
        else:
            messages.add_message(request, messages.constants.ERROR, form.errors)
            return redirect(reverse('sign-up-contributeur'))
    form = NewUserForm()
    return render(request, 'image_bank/contributeur/sign-up-cover.html', {'form': form})


def signin_contributeur(request):
    if request.method == 'POST':
        form = RegisteredUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = CustomUser.objects.get(email=data.get('email'))
                if user.check_password(data.get('password')):
                    login(request, user)
                    return redirect(reverse('index-contributeur'))
                else:
                    messages.add_message(request, messages.constants.ERROR, 'Mot de passe incorrect')
                return redirect(reverse('sign-in-contributeur'))
            except CustomUser.DoesNotExist:
                messages.add_message(request, messages.constants.ERROR, 'Utilisateur n\'existe pas')
                return redirect(reverse('sign-in-contributeur'))
        else:
            messages.add_message(request, messages.constants.ERROR, form.errors)
            return redirect(reverse('sign-in-contributeur'))
    form = RegisteredUserForm()
    return render(request, 'image_bank/contributeur/sign-in-cover.html', {'form': form})


def index_contributeur(request):
    return render(request, 'image_bank/contributeur/index.html')


def images_contributeur(request):
    paginator = Paginator(Image.objects.all(), 4)
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)
    return render(request, 'image_bank/contributeur/mes-images.html', {'images': page_object})


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('sign-in'))
    
# define a function-based view that return a modelForm from an id sent by the client
def get_json_image(request, id):
    try:
        image = Image.objects.get(pk=id)
    except Image.DoesNotExist:
        return JsonResponse({"message": "Image non trouvée", "code_message": 404}, status=404)
    
    serializer = ImageSerializer(instance=image)
    return JsonResponse({"image": serializer.data, "code_message": 200}, status=200)


def get_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return JsonResponse({"users": serializer.data, "code_message": 200}, status=200)
    

@login_required
def upload_image(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        tags_data = post_data.get('tags')
        licence = post_data.get('licence')
        if tags_data:
            del post_data['tags']
            tags = [Tag.objects.create(name=tag_name) for tag_name in tags_data.split(',')]
        else:
            tags = []
        
        form = ImageForm(post_data, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit=False)
            try:
                with PImage.open(request.FILES['image']) as image:
                    instance.width = image.width
                    instance.height = image.height
                    instance.format = image.format
                    instance.taille = image.size
                # To change later with the current user's id
                instance.contributor = CustomUser.objects.get(pk=request.user.id)
                instance.save()
            except IntegrityError:
                return JsonResponse({"message": "Utilisateur existe déjà", "code_message": 200}, status=200)
            if licence:
                instance.licence = Licence.objects.get(pk=int(licence)).name
            if tags:
                instance.tags.add(*tags)
            instance.save()
            return JsonResponse({"message": "Image chargée avec succès", "code_message": 200}, status=200)
        else:
            return JsonResponse({"message": "Formulaire non valide", "code_message": 400}, status=400)
    else:
        return JsonResponse({"message": "Méthode non autorisée", "code_message": 400}, status=400)


# define a function-based view used to update an image sent by the client using it's id and form data
@login_required
def update_image(request, id):
    if request.method == 'POST':
        image = get_object_or_404(Image, pk=id)
        post_data = request.POST.copy()
        tags_data = post_data.get('tags')
        licence = post_data.get('licence')
        if tags_data:
            del post_data['tags']
            tags = [Tag.objects.create(name=tag_name) for tag_name in tags_data.split(',')]
        else:
            tags = []

        form = ImageForm(post_data, request.FILES, instance=image)
        if form.is_valid():
            instance = form.save(commit=False)
            try:
                # To change later with the current user's id
                instance.contributor = CustomUser.objects.get(pk=request.user.id)
                if licence:
                    instance.licence = Licence.objects.get(pk=int(licence)).name
                else:
                    instance.licence = ""
                if tags:
                    instance.tags.set(tags)
                instance.save()
                return JsonResponse({"message": "Image modifiée avec succès", "code_message": 200}, status=200)
            except CustomUser.DoesNotExist:
                return JsonResponse({"message": "Utilisateur n'existe pas", "code_message": 400}, status=400)
            except Licence.DoesNotExist:
                return JsonResponse({"message": "Licence non trouvée", "code_message": 400}, status=400)
        else:
            print(form.errors)
            return JsonResponse({"message": "Formulaire non valide", "code_message": 400}, status=400)
    else:
        return JsonResponse({"message": "Méthode non autorisée", "code_message": 400}, status=400)