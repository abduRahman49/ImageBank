from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User


# This is a custom model used for authentication purpose
class CustomUser(User):
    class ROLE(models.TextChoices):
        CONTRIB = "C", _("Contributor")
        USER = "U", _("User")
    role = models.CharField(max_length=10, choices=ROLE.choices, default=ROLE.USER)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    

class Payment(models.Model):
    price = models.FloatField()
    currency = models.CharField(max_length=3)
    image_title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")


class Licence(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Image(models.Model):
    # When an image is uploaded to the platform, it has the following three states
    class STATUS(models.TextChoices):
        PENDING = "P", _("Pending")
        VALIDATED = "V", _("Validated")
        REJECTED = "R", _("Rejected")
        
    # Images are also applicable to licences
    class LICENCES(models.TextChoices):
        ALL_RIGHTS_RESERVED = "ARR", _("Tous droits réservés")
        PUBLIC_DOMAIN = "PD", _("Domaine public")
        CREATIVE_COMMONS = "CC", _("Creative commons")
        CREATIVE_COMMONS_NM = "CCNM", _("Creative commons - Pas de modification")
        CREATIVE_COMMONS_NM_NCU = "CCNMNCU", _("Creative commons - Pas d'utilisation commerciale, Pas de modification")
        CREATIVE_COMMONS_NM_PCII = "CCNMNPCCI", _("Creative commons - Pas d'utilisation commerciale, Partage des conditions initiales à l'identique")
        CREATIVE_COMMONS_PCII = "CCNPCCI", _("Creative commons - Partage des conditions initiales à l'identique")
        
    name = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    watermark = models.ImageField(upload_to='watermarks/', null=True)
    description = models.TextField(blank=True)
    taille = models.IntegerField(null=True)
    format = models.CharField(max_length=200)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    orientation = models.IntegerField(null=True)
    status = models.CharField(max_length=10, choices=STATUS.choices, default=STATUS.PENDING)
    payment_required = models.BooleanField(default=False)
    licence = models.CharField(max_length=100, blank=True)
    # licence = models.ForeignKey(Licence, on_delete=models.CASCADE, related_name='licences')
    price = models.FloatField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    contributor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images')
    