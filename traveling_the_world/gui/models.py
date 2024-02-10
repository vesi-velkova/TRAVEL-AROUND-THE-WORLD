from django.db import models

class DreamDestinations(models.Model):
    destination_name = models.CharField(max_length=90) 
    # The city with longest name is Taumatawhakatangihangakoauauotamate 
    # aturipukakapiki-maungahoronukupokaiwhenuakitnatahu (85 chars length)
    country = models.CharField(max_length=50)
    # Country with longest name is United Kingdom of Great Britain and Northern Ireland (46 letters).