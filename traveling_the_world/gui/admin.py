from django.contrib import admin
from .models import DreamDestinations, DreamDestinationsList

class DreamDestinationsAdmin(admin.ModelAdmin):
    model = DreamDestinations
    ordering = ('country', 'destination_name')
    search_fields = ('destination_name',)
    list_display = ('destination_name', 'country')
    fields = ('destination_name', 'country')


class DreamDestinationsListAdmin(admin.ModelAdmin):
    model = DreamDestinationsList
    ordering = ('dream_destinations_list', 'owner')
    search_fields = ('dream_destinations_list',)
    list_display = ('dream_destinations_list', 'owner')
    fields = ('dream_destinations_list', 'owner')


admin.site.register(DreamDestinations, DreamDestinationsAdmin)
admin.site.register(DreamDestinationsList, DreamDestinationsListAdmin)
