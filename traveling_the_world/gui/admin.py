from django.contrib import admin
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


admin.site.register(Destination, DestinationAdmin)
admin.site.register(DreamDestinationsList, DreamDestinationsListAdmin)

class CountryAdmin(admin.ModelAdmin):
    model = Country
    ordering = ('countries_list', 'name', 'cities_to_visit')
    search_fields = ('countries_list', 'name')
    list_display = ('name', 'visited', 'countries_list')
    fields = ('name', 'cities_to_visit', 'visited', 'countries_list')


class CountriesListAdmin(admin.ModelAdmin):
    model = CountryList
    ordering = ('countries_in_the_world', 'owner')
    search_fields = ('countries_in_the_world',)
    list_display = ('countries_in_the_world', 'owner')
    fields = ('countries_in_the_world', 'owner')

admin.site.register(Country, CountryAdmin)
admin.site.register(CountryList, CountriesListAdmin)