import random
import countryinfo

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.http import HttpResponseNotFound, JsonResponse
from . import places
from .models import DreamDestinationsList, Destination
from .forms import AddDestinationForm

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

@login_required(login_url='/login/')
def detailed_page(request):
    """Individual page with details for every dream destination."""
    try:
        destination = Destination.objects.get(pk=request.GET['id'])
    except (KeyError, Destination.DoesNotExist):
        return HttpResponseNotFound('Invalid link. No ID found.')
    place_obj = places.PlacesUtilities().find_places_given_place_type_and_radius(destination)
    context = {
        'destination_name': destination.destination_name,
        # When we are searching for a city, we expect this function to return a list with 1 place.
        'photo': place_obj[0].get_photo_url() 
    }
    detailed_info_keys = ['name', 'subregion', 'region', 'capital', 'currencies', 
                          'timezones', 'languages','population', 'wiki']
    for item in detailed_info_keys:
        context[item] = countryinfo.CountryInfo(destination.country).info()[item]

    return render(request, 'details.html', context)
    
@login_required(login_url='/login/')
def remove_item(request):
    """Remove an item."""
    try:
        item = Destination.objects.get(pk=request.GET['id'])
        # Ensure that a user can't touch other people's stuff
        if item.list_name.owner != request.user:
            return HttpResponseNotFound('Invalid link.')
    except (KeyError, Destination.DoesNotExist):
        return HttpResponseNotFound('Invalid link.')
    item.delete()
    return redirect('/dream_destinations/')

@login_required(login_url='/login/')
def add_item(request):
    """Add an item."""
    try:
        destination_name = request.POST['destination_name']
        country = request.POST['country']
        list_name = DreamDestinationsList.objects.filter(owner=request.user).get()
    except (KeyError, ValueError, DreamDestinationsList.DoesNotExist):
        return HttpResponseNotFound('Invalid link.')
    form = AddDestinationForm({'destination_name': destination_name,
                                'country': country,
                                'list_name': list_name})
    if form.is_valid():
        form.save()
    return redirect('/dream_destinations/')