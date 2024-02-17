import pycountry

from django.contrib import admin
from django.contrib.auth.models import User
from .models import Destination, DreamDestinationsList
from .models import Country, CountryList

class DestinationAdmin(admin.ModelAdmin):
    model = Destination
    ordering = ('list_name', 'country', 'destination_name')
    search_fields = ('destination_name', 'list_name')
    list_display = ('list_name', 'destination_name', 'country')
    fields = ('list_name', 'destination_name', 'country')


class DreamDestinationsListAdmin(admin.ModelAdmin):
    model = DreamDestinationsList
    ordering = ('dream_destinations_list', 'owner')
    search_fields = ('dream_destinations_list',)
    list_display = ('dream_destinations_list', 'owner')
    fields = ('dream_destinations_list', 'owner')

    @staticmethod
    def populate_database(user):
        object = DreamDestinationsList(dream_destinations_list = "DREAM DESTINATIONS", owner = user)
        object.save()

admin.site.register(Destination, DestinationAdmin)
admin.site.register(DreamDestinationsList, DreamDestinationsListAdmin)

class CountryAdmin(admin.ModelAdmin):
    model = Country
    ordering = ('name', 'countries_list', 'cities_to_visit')
    search_fields = ('countries_list', 'name')
    list_display = ('name', 'visited', 'countries_list')
    fields = ('name', 'cities_to_visit', 'visited', 'countries_list')

    @staticmethod
    def populate_database(user):
        for country in pycountry.countries:
            if country.name == 'United States':
                cities_count = 250
            else:
                cities_count = 30
            object = Country(name = country.name, cities_to_visit = cities_count, visited = False, 
                             countries_list = CountryList.objects.filter(owner = user).get())
            object.save()
            
        
class CountriesListAdmin(admin.ModelAdmin):
    model = CountryList
    ordering = ('countries_in_the_world', 'owner')
    search_fields = ('countries_in_the_world',)
    list_display = ('countries_in_the_world', 'owner')
    fields = ('countries_in_the_world', 'owner')
    
    @staticmethod
    def populate_database(user):
        object = CountryList(countries_in_the_world = 'Countries List', owner = user)
        object.save()

admin.site.register(Country, CountryAdmin)
admin.site.register(CountryList, CountriesListAdmin)

