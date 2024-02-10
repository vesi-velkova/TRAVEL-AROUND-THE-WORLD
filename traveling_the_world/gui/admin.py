from django.contrib import admin
from .models import DreamDestinations

class DreamDestinationsAdmin(admin.ModelAdmin):
    model = DreamDestinations
    ordering = ('country', 'destination_name')
    search_fields = ('destination_name',)
    list_display = ('destination_name', 'country')
    fields = ('destination_name', 'country')

admin.site.register(DreamDestinations, DreamDestinationsAdmin)
