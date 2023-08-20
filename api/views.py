from rest_framework import generics
from image_bank.models import Image, Licence
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ImageSerializer, LicenceSerializer
from .utilities import ImagePagination, LicencePagination

# Create your views here.
class ImageModelViewset(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    pagination_class = ImagePagination
    queryset = Image.objects.all()
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        status = request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class LicenceModelViewset(viewsets.ModelViewSet):
    serializer_class = LicenceSerializer
    pagination_class = LicencePagination
    queryset = Licence.objects.all()