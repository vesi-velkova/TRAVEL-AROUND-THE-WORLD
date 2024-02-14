import os
import pycountry
import urllib
import requests
import geonamescache
import countryinfo

from geopy.geocoders import Nominatim
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

class Place:
    """This class represents either a country/city or a tourist attraction."""
    
    def __init__(self, place_id, geometry_tuple, name, is_attraction):
        self.place_id = place_id
        self.latitude, self.longitude = geometry_tuple
        self.name = name
        ''' If this boolean is True, we will try to extract information such as opening hours,
        formatted_phone_number, ratings and user_ratings_total.'''
        self.is_attraction = is_attraction
        self.formatted_phone_number = None
        self.opening_hours = None
        self.rating = 0
        self.user_ratings_total = 0
        
    def set_details(self):
        URL_DETAILS = 'https://maps.googleapis.com/maps/api/place/details/json'
        parameters = {'place_id':self.place_id, 'key': API_KEY}
        curr_request = requests.get(url = URL_DETAILS, params = parameters)
        detailed_data = curr_request.json()
        
        self.formatted_address = detailed_data['result']['formatted_address']
        self.types = detailed_data['result']['types']
        self.photo_reference = detailed_data['result']['photos'][0]['photo_reference']

        if self.is_attraction:
            # There is no else, because they have a default value None or 0.
            try:
                self.rating = detailed_data['result']['rating']
                self.user_ratings_total = detailed_data['result']['user_ratings_total']
            except:
                print("This place has no rating and/or user_ratings. It won't be suggested for a visit.")
            try:
                with detailed_data['result']['formatted_phone_number'] as phone_number:
                    self.formatted_phone_number = phone_number
                with detailed_data['result']['opening_hours'] as opening_hours:
                    self.opening_hours = opening_hours
            except:
                print("This place has no formatted_phone_number and/or information about openning hours.")

    def get_photo_reference(self):
        try:
            photo = self.photo_reference
        except AttributeError:
            self.set_details()
            photo = self.photo_reference
        return photo
    
    def get_photo_url(self):
        URL_PHOTO = 'https://maps.googleapis.com/maps/api/place/photo?'
        parameters = {'maxwidth':'4000', 'photo_reference':self.get_photo_reference(), 'key': API_KEY}
        photo_request = URL_PHOTO + urllib.parse.urlencode(parameters)
        response = requests.get(photo_request)
        return response.url
    
    def get_rating_tuple(self):
        if self.is_attraction:
            try:
                address = self.formatted_address
            except AttributeError:
                # The details have not been set if the attribute formatted_adress doesn't exist,
                # therefore we don't know the rating of the place.
                self.set_details()
        rating_tuple = (self.rating, self.user_ratings_total)
            
        return rating_tuple
            
    
class PlacesUtilities:
    
    def __init__(self):
        self.geonames = geonamescache.GeonamesCache()
        self.geolocator = Nominatim(user_agent="travel_around_the_world")
        
    def get_longitude_latitude_tuple(self, place_str):
        """This function is able to extract the longitude and latitude 
        only if place_str is a valid city or country. """
        location = self.geolocator.geocode(place_str)
        if location is not None:
            return (location.latitude, location.longitude)
        raise AttributeError("Unable to extract latitude and longitude of this location.")
    
    def find_places_given_place_type_and_radius(self, place, radius=50000, type = ""):
        """This function has to find via textsearch all of the places of a certain type around a given place
        (given city and radius). Only information about the place_id, geometry/location and name will be saved.
        If type is not specified, then the query will be only for a specified place (country, province or city).
        """
        # Basic url for text search via Google Maps API - Places.
        URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        # When the city is specified in the query, it overrides the location parameter.
        # If we pass the desired longitude and latitude, it is possible for them to be overriden by
        # other factors such as nearby location.
        if type == '':
            query = place
            parameters = {'query':query, 'key': API_KEY}
            curr_request = requests.get(url = URL, params = parameters)
            data = curr_request.json()
            place_id = data['results'][0]['place_id']
            geometry = (data['results'][0]['geometry']['location']['lat'], 
                        data['results'][0]['geometry']['location']['lng'])
            name = data['results'][0]['name']
            return [Place(place_id, geometry, name, False)]
       
        query = type + ' in ' + place
        parameters = {'query':query, 'radius': radius, 'key':API_KEY}
        curr_request = requests.get(url = URL, params = parameters)
        data = curr_request.json()
        list_of_attractions = []
        for attraction in data['results']:
            place_id = attraction['place_id']
            geometry = (attraction['geometry']['location']['lat'], attraction['geometry']['location']['lng'])
            name = attraction['name']
            curr_place = Place(place_id, geometry, name, True)
            list_of_attractions.append(curr_place)
        return list_of_attractions

    def find_biggest_cities_by_country_name(self, country_name):
        """This function has to retrieve the names of top 30 of the biggest cities in a country by population.
        In case that the specified country has less than 30 cities with population above 15000 people, all of 
        them will be appended to the list."""
        list_of_cities = []
        try:
            country = pycountry.countries.lookup(country_name)
        except LookupError:
            print(f"Can not find cities, because {country_name} is invalid country.")
            raise
        country_code = countryinfo.CountryInfo(country_name).iso()['alpha2']
        for city in self.geonames.get_cities().values():
            if city['countrycode'] == country_code:
                list_of_cities.append(city)
        if country_code == 'US':
            usa_cities = []
            for state in self.geonames.get_us_states().keys():
                curr_state_list = [city for city in list_of_cities if city['admin1code'] == state]
                curr_state_list.sort(reverse=True,key=lambda item: item.get('population'))
                usa_cities.extend(curr_state_list[0:5])
            usa_cities.sort(reverse=True,key=lambda item: item.get('population'))
            return [city['name'] for city in usa_cities]
        list_of_cities.sort(reverse=True,key=lambda item: item.get('population'))
        return [city['name'] for city in list_of_cities[0:30]]
        
    