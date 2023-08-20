import json
from django.shortcuts import render
from .forms import ImageForm
from .models import Licence, Tag, CustomUser, Image
from api.serializers import ImageSerializer
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    form = ImageForm()
    return render(request, 'image_bank/index.html', {'form': form})


# define a function-based view that return a modelForm from an id sent by the client
def get_json_image(request, id):
    try:
        image = Image.objects.get(pk=id)
    except Image.DoesNotExist:
        return JsonResponse({"message": "Image non trouvée", "code_message": 404}, status=404)
    
    serializer = ImageSerializer(instance=image)
    return JsonResponse({"image": serializer.data, "code_message": 200}, status=200)


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
                # To change later with the current user's id
                instance.contributor = CustomUser.objects.get(pk=3)
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
                instance.contributor = CustomUser.objects.get(pk=3)
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