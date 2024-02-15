from django.contrib import admin
from .models import Destination, DreamDestinationsList
from .models import Country

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
    ordering = ('name', 'cities_to_visit')
    search_fields = ('name',)
    list_display = ('name', 'visited')
    fields = ('name', 'cities_to_visit', 'visited')

admin.site.register(Country, CountryAdmin)