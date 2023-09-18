import numpy as np
import tempfile
from PIL import Image as PImage
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ImageForm, NewUserForm, RegisteredUserForm
from .models import CustomUser, Image
from api.serializers import ImageSerializer, CustomUserSerializer
from api.utilities import convert_to_format, resize_to_resolution
from taggit.models import Tag
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, HttpResponse
from django.core.paginator import Paginator


resolutions = {
    'low': Q(taille__lt=480000),
    'medium': Q(taille__gte=480000, taille__lt=2073600),
    'high': Q(taille__gte=2073600)
}

paiements = {
    "0": False,
    "1": True
}

# Create your views here.
@login_required
def index(request):
    form = ImageForm()
    return render(request, 'image_bank/index.html', {'form': form})


def login_users(request):
    return render(request, 'image_bank/index.html')

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
                    return redirect(reverse('upload-contributeur'))
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


def signup_user(request):
    print("entered the function")
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = CustomUser.objects.create_user(data.get('username'), data.get('email'), data.get('password'))
                user.role = "U"
                user.save()
                return redirect(reverse('sign-in-user'))
            except IntegrityError:
                messages.add_message(request, messages.constants.ERROR, 'Utilisateur déjà existant')
                return redirect(reverse('sign-up-user'))
        else:
            messages.add_message(request, messages.constants.ERROR, form.errors)
            return redirect(reverse('sign-up-user'))
    form = NewUserForm()
    return render(request, 'image_bank/utilisateur/sign-up-cover.html', {'form': form})


def signin_user(request):
    if request.method == 'POST':
        form = RegisteredUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = CustomUser.objects.get(email=data.get('email'))
                if user.check_password(data.get('password')):
                    login(request, user)
                    return redirect(reverse('user-index'))
                else:
                    messages.add_message(request, messages.constants.ERROR, 'Mot de passe incorrect')
                return redirect(reverse('sign-in-user'))
            except CustomUser.DoesNotExist:
                messages.add_message(request, messages.constants.ERROR, 'Utilisateur n\'existe pas')
                return redirect(reverse('sign-in-user'))
        else:
            messages.add_message(request, messages.constants.ERROR, form.errors)
            return redirect(reverse('sign-in-user'))
    form = RegisteredUserForm()
    return render(request, 'image_bank/utilisateur/sign-in-cover.html', {'form': form})


@login_required
def user_index(request):
    print("Accessed user index view")
    paginator = Paginator(Image.objects.filter(status="V"), 4)
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)
    expression = Q(format=None) | Q(format="")
    formats = Image.objects.exclude(expression).values_list('format', flat=True).distinct()
    tags = Tag.objects.filter(image__isnull=False).distinct()
    print("Accessed the end")
    return render(request, 'image_bank/utilisateur/accueil.html', {'images': page_object, 'formats': formats, 'tags': tags})


@login_required
def index_contributeur(request):
    form = ImageForm()
    return render(request, 'image_bank/contributeur/charger-images.html', {'form': form})


@login_required
def images_contributeur(request):
    paginator = Paginator(Image.objects.filter(contributor=request.user), 4)
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)
    form = ImageForm()
    return render(request, 'image_bank/contributeur/mes-images.html', {'images': page_object, 'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
    
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
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            try:
                with PImage.open(request.FILES['image']) as image:
                    instance.width = image.width
                    instance.height = image.height
                    instance.format = image.format
                    instance.taille = np.multiply(*image.size)
                # To change later with the current user's id
                instance.contributor = CustomUser.objects.get(pk=request.user.id)
                instance.save()
                form.save_m2m()
                return JsonResponse({"message": "Image chargée avec succès", "code_message": 200}, status=200)
            except IntegrityError:
                return JsonResponse({"message": "Utilisateur existe déjà", "code_message": 200}, status=200)
        else:
            return JsonResponse({"message": f"{form.errors}", "code_message": 400}, status=400)
    else:
        form = ImageForm()
        return render(request, "image_bank/contributeur/charger-images.html", {'form': form})


# define a function-based view used to update an image sent by the client using it's id and form data
@login_required
def update_image(request, id):
    from taggit.utils import parse_tags
    
    if request.method == 'POST':
        image = get_object_or_404(Image, pk=id)
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            instance = form.save(commit=False)
            try:
                instance.contributor = CustomUser.objects.get(pk=request.user.id)
                new_tags = parse_tags(form.cleaned_data['new_tags'])
                
                for tag in new_tags:
                    image.new_tags.add(tag)
                instance.save()
                form.save_m2m()
                return JsonResponse(
                    {"message": "Image modifiée avec succès", "code_message": 200},
                )
            except CustomUser.DoesNotExist:
                return JsonResponse({"message": "Utilisateur n'existe pas", "code_message": 400}, status=400)
        else:
            return JsonResponse({"message": f"{form.errors}", "code_message": 400}, status=400)
    else:
        return JsonResponse({"message": "Méthode non autorisée", "code_message": 400}, status=400)
    

@login_required
def delete_image(request, id):
    image = get_object_or_404(Image, pk=id)
    image.delete()
    return JsonResponse(
        {"message": "Image supprimée avec succès", "code_message": 200},
    )
    

@login_required
def accueil_images(request):
    paginator = Paginator(Image.objects.all(), 4)
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)
    expression = Q(format=None) | Q(format="")
    formats = Image.objects.exclude(expression).values_list('format', flat=True).distinct()
    tags = Tag.objects.filter(image__isnull=False).distinct()
    return render(request, 'image_bank/contributeur/accueil.html', {'images': page_object, 'formats': formats, 'tags': tags})


@login_required
def search_images(request, id=None):
    if request.method == "POST":
        resolution = request.POST.get('resolution')
        format_image = request.POST.get('format')
        paiement = request.POST.get('paiement')
        
        queryset = Image.objects.filter(status='V')
        if resolution is not None and resolution != "":
            queryset = queryset.filter(resolutions.get(resolution))
        if format_image is not None and format_image != "":
            queryset = queryset.filter(format__icontains=format_image)
        if paiement is not None and paiement != "":
            queryset = queryset.filter(payment_required=paiements.get(paiement))
        
        paginator = Paginator(queryset, 4)
        page_number = request.GET.get('page', 1)
        page_object = paginator.get_page(page_number)
        return render(request, 'image_bank/utilisateur/resultats-recherche.html', {'images': page_object})
    elif request.method == "GET":
        tag = get_object_or_404(Tag, pk=id)
        queryset = Image.objects.filter(new_tags__name__in=[tag.name])
        paginator = Paginator(queryset, 4)
        page_number = request.GET.get('page', 1)
        page_object = paginator.get_page(page_number)
        return render(request, 'image_bank/utilisateur/resultats-recherche.html', {'images': page_object})
    else:
        return HttpResponse("Method not Allowed!")
    

@login_required
def detail_image(request, id):
    image = get_object_or_404(Image, pk=id)
    return render(request, "image_bank/utilisateur/image-detail.html", {'image': image})


@login_required
def download_image(request, id):
    from io import BytesIO
    from django.core.files import File
    
    image_format = request.POST.get('image_format')
    image_resolution = request.POST.get('image_resolution')
    image = get_object_or_404(Image, pk=id)
    
    converted_image_path = convert_to_format(image.image.url, image_format)
    final_image_output = resize_to_resolution(converted_image_path, image_resolution, image_format)
    
    image.downloaded.save(f'download.{image_format}', File(open(final_image_output, 'rb')), save=True)

    response = f'''
        <a download href="{image.downloaded.url}" class="btn bg-gradient-dark mb-0 mt-lg-auto w-100">Cliquez ici pour télécharger</a>
    '''
    return HttpResponse(response)