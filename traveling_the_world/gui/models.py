from django.db import models
from django.contrib.auth.models import User


class DreamDestinationsList(models.Model):
    dream_destinations_list = models.CharField(max_length = 50, default = "DREAM DESTINATIONS")
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.owner.username} - {self.dream_destinations_list}"
    
class Destination(models.Model):
    destination_name = models.CharField(max_length=90) 
    # The city with longest name is Taumatawhakatangihangakoauauotamate 
    # aturipukakapiki-maungahoronukupokaiwhenuakitnatahu (85 chars length)
    country = models.CharField(max_length=50)
    # Country with longest name is United Kingdom of Great Britain and Northern Ireland (46 letters).
    list_name = models.ForeignKey(DreamDestinationsList, on_delete=models.CASCADE,
                                  related_name='items')
    
    def __str__(self):
        return f"{self.destination_name}, {self.country}"


class CountryList(models.Model):
    countries_in_the_world = models.CharField(max_length = 50, default = "Countries List")
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.owner.username} - {self.countries_in_the_world}"
    
class Country(models.Model):
    name = models.CharField(max_length=50)
    cities_to_visit = models.IntegerField(default=1)
    visited = models.BooleanField(default=False)
    countries_list = models.ForeignKey(CountryList, on_delete=models.CASCADE,
                                       related_name='countries')

    def __str__(self):
        return f"{self.name}"