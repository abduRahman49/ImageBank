from rest_framework.pagination import PageNumberPagination
from image_bank.models import Image, Licence
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ImageSerializer, LicenceSerializer
from .utilities import ImagePagination, LicencePagination

# Create your views here.
class ImageModelViewset(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    pagination_class = ImagePagination
    queryset = Image.objects.all()


class ImageSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = Image.objects.filter(status='V')
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ImageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class LicenceModelViewset(viewsets.ModelViewSet):
    serializer_class = LicenceSerializer
    pagination_class = LicencePagination
    queryset = Licence.objects.all()