from rest_framework.pagination import PageNumberPagination
from image_bank.models import Image, Licence, CustomUser
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ImageSerializer, LicenceSerializer, CustomUserSerializer
from .utilities import ImagePagination, LicencePagination
from django.shortcuts import render
import json

# Create your views here.
class ImageModelViewset(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    pagination_class = ImagePagination
    queryset = Image.objects.all()


class ImageSearchAPIView(APIView):
    def post(self, request, *args, **kwargs):
        auteur = request.POST.get('auteur')
        licence = request.POST.get('licence')
        type_image = request.POST.get('type')
        print('Auteur, licence et type', auteur, licence, type_image)
        # paginator = PageNumberPagination()
        # paginator.page_size = 10
        queryset = Image.objects.filter(status='P')
        if auteur:
            queryset = queryset.filter(auteur=auteur)
        if licence:
            queryset = queryset.filter(licence=licence)
        if type_image:
            queryset = queryset.filter(payment_required=json.loads(type_image))
        # result_page = paginator.paginate_queryset(queryset, request)
        # serializer = ImageSerializer(result_page, many=True)
        # serializer = ImageSerializer(queryset, many=True)
        # paginator.get_paginated_response(serializer.data)
        return render(request, 'image_bank/images_results.html', {'images': ['abdou', 'mouss', 'samba']})

class LicenceModelViewset(viewsets.ModelViewSet):
    serializer_class = LicenceSerializer
    pagination_class = LicencePagination
    queryset = Licence.objects.all()
    

class AuteurModelViewset(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = LicencePagination
    queryset = CustomUser.objects.only('username')