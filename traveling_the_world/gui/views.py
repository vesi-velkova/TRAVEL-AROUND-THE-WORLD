import random

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import DreamDestinationsList
from django.http import HttpResponseNotFound
from . import places
import requests

class MainPagesViews:
    @login_required(login_url='/login/')
    def home_page(request):
        """Welcome page."""
        context = {
            'username': request.user.first_name or request.user.username
        }
        return render(request, 'home_page.html', context)

    @login_required(login_url='/login/')
    def dream_destinations_view(request):
        """Dream destinations page."""
        try:
            destination_list = DreamDestinationsList.objects.filter(owner=request.user)
        except (KeyError, DreamDestinationsList.DoesNotExist):
            return HttpResponseNotFound('Invalid link. No dream destinations.')
        if not len(destination_list.get().items.all()):
            place_obj = places.PlacesUtilities().find_places_given_place_type_and_radius('Burgas, Bridge')
        else:
            index = random.randint(1, len(destination_list.get().items.all()))
            destination = destination_list.get().items.all()[index - 1]
            place_obj = places.PlacesUtilities().find_places_given_place_type_and_radius(destination)
        context = {
            'name': destination_list.values().get()['dream_destinations_list'],
            'items': destination_list.get().items.all(),
            'photo': place_obj[0].get_photo_url()
        }
        return render(request, 'dream_list.html', context)

    @login_required(login_url='/login/')
    def logout_view(request):
        """
        Logout view. Login is required. 
        Redirects to the login page. 
        """
        logout(request)
        return redirect("/login/")
    
    