from rest_framework import serializers
from image_bank.models import Image, Tag, Licence


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = ['id', 'name', 'description']


class ImageSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    # licence = LicenceSerializer()
    class Meta:
        model = Image
        fields = ['id', 'image', 'auteur', 'name', 'description', 'price', 'licence', 'tags']