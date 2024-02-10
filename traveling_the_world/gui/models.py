from django.db import models
from django.contrib.auth.models import User


class DreamDestinationsList(models.Model):
    dream_destinations_list = models.CharField(max_length = 50, default = "DREAM DESTINATIONS")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Destination(models.Model):
    destination_name = models.CharField(max_length=90) 
    # The city with longest name is Taumatawhakatangihangakoauauotamate 
    # aturipukakapiki-maungahoronukupokaiwhenuakitnatahu (85 chars length)
    country = models.CharField(max_length=50)
    # Country with longest name is United Kingdom of Great Britain and Northern Ireland (46 letters).
    list_name = models.ForeignKey(DreamDestinationsList, on_delete=models.CASCADE, null=True)