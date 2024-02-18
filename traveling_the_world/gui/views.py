import random
import countryinfo

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login
from django.http import HttpResponseNotFound, JsonResponse
from .forms import AddDestinationForm, RegisterUserForm

from .places import PlacesUtilities
from . import models
from . import admin

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
        destination_list = models.DreamDestinationsList.objects.filter(owner=request.user)
        length = len(destination_list.get().items.all())
    except (KeyError, models.DreamDestinationsList.DoesNotExist):
        return HttpResponseNotFound('Invalid link. No dream destinations.')

    if not length:
        # Show background image of Burgas, if the list of dream destinations is empty.
        place_obj = PlacesUtilities.find_places_given_place_type_and_radius('Burgas, Bridge')
    else:
        # Select random destination from the list and verify does it exist.
        index = random.randint(1, len(destination_list.get().items.all()))
        destination = destination_list.get().items.all()[index - 1]
        try:
            place_obj = PlacesUtilities.find_places_given_place_type_and_radius(destination)
        except:
            return HttpResponseNotFound(f"'{destination}' is invalid or there is lack of information about it.")

    context = {
        'name': destination_list.values().get()['dream_destinations_list'],
        'items': destination_list.get().items.all(),
    }
    try:
        picture = place_obj[0].get_photo_url()
        context['photo'] = picture
    except KeyError:
        # There will be no background picture.
        pass

    return render(request, 'dream_list.html', context)

@login_required(login_url='/login/')
def find_destination_view(request):
    """View for the Destination tab."""
    try:
        countries_list = models.CountryList.objects.filter(owner=request.user)
        countries_items = countries_list.get().countries.all()
    except (KeyError, models.CountryList.DoesNotExist):
        return HttpResponseNotFound('Invalid link. No dream destinations.')

    most_visited_country = admin.CountryAdmin.find_most_visited_country()
    capital = countryinfo.CountryInfo(most_visited_country).capital()
    country_obj= PlacesUtilities.find_places_given_place_type_and_radius(capital)

    context = {
        'items': countries_items,
    }
    try:
        picture = country_obj[0].get_photo_url()
        context['photo'] = picture
    except KeyError:
        # There will be no background picture.
        pass

    return render(request, 'destination.html', context)

@login_required(login_url='/login/')
def detailed_page(request):
    """Individual page with details for every dream destination."""
    try:
        destination = models.Destination.objects.get(pk=request.GET['id'])
    except (KeyError, models.Destination.DoesNotExist):
        return HttpResponseNotFound('Invalid link. No ID found.')
    try:
        place_obj = PlacesUtilities().find_places_given_place_type_and_radius(destination)
    except:
        return HttpResponseNotFound(f"'{destination}' is invalid or there is lack of information about it.")

    context = {
        'destination_name': destination.destination_name,
    }

    try:
        picture = place_obj[0].get_photo_url()
        context['photo'] = picture
    except KeyError:
        # There will be no background picture.
        pass

    detailed_info_keys = ['name', 'subregion', 'region', 'capital', 'currencies',
                           'languages','population', 'wiki']
    for item in detailed_info_keys:
        context[item] = countryinfo.CountryInfo(destination.country).info()[item]

    return render(request, 'details.html', context)

@login_required(login_url='/login/')
def remove_item(request):
    """Remove an item from the list of dream destinations of the user."""
    try:
        item = models.Destination.objects.get(pk=request.GET['id'])
        # Ensure that a user can't touch other people's stuff
        if item.list_name.owner != request.user:
            return HttpResponseNotFound('Invalid link.')
    except (KeyError, models.Destination.DoesNotExist):
        return HttpResponseNotFound('Invalid link.')
    item.delete()
    return JsonResponse({'state': 'removed'})

@login_required(login_url='/login/')
def add_item(request):
    """Add an item to the list with dream destinations of the user."""
    try:
        destination_name = request.POST['destination_name']
        country = request.POST['country']
        list_name = models.DreamDestinationsList.objects.filter(owner=request.user).get()
    except (KeyError, ValueError, models.DreamDestinationsList.DoesNotExist):
        return HttpResponseNotFound('Invalid link.')
    if not PlacesUtilities.is_country_valid(country):
        return HttpResponseNotFound('Please, enter a valid country in the world.')
    form = AddDestinationForm({'destination_name': destination_name,
                                'country': country,
                                'list_name': list_name})
    if form.is_valid():
        form.save()
    return redirect('/dream_destinations/')

@login_required(login_url='/login/')
def logout_view(request):
    """
    Logout view. Login is required. 
    Redirects to the login page. 
    """
    logout(request)
    return redirect("/login/")

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            admin.CountriesListAdmin.populate_database(user)
            admin.CountryAdmin.populate_database(user)
            admin.DreamDestinationsListAdmin.populate_database(user)
            return redirect('/')
    else:
        form = RegisterUserForm()
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)

@login_required(login_url='/login')
def visit_item_view(request):
    """Toggle between visited states of a country."""
    try:
        item = models.Country.objects.get(pk=request.GET['id'])
        state = request.GET['state'] == '1'
        # Ensure that a user can't touch other people's stuff
        if item.countries_list.owner != request.user:
            return HttpResponseNotFound('Invalid link.')
    except (KeyError, models.Country.DoesNotExist):
        return HttpResponseNotFound('Invalid link.')
    item.visited = state
    item.save()
    return JsonResponse({'state': item.visited})
