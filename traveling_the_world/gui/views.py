import random

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import DreamDestinationsList
from django.http import HttpResponseNotFound
from . import places

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
        index = random.randint(1, len(destination_list.get().items.all()))
        destination = destination_list.get().items.all()[index - 1]
        place_id = places.PlacesUtilities().find_places_given_place_type_and_radius(destination, 50000)
        photo_request = places.PlacesUtilities().get_url_place_photo(place_id)
        print(photo_request)
        context = {
            'name': destination_list.values().get()['dream_destinations_list'],
            'items': destination_list.get().items.all(),
            'photo': photo_request
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
    
    