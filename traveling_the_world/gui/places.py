import os
import pycountry
import requests
import geonamescache
import countryinfo

from geopy.geocoders import Nominatim
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

class PlacesUtilities:
    
    def __init__(self):
        # self.gmaps = googlemaps.Client(API_KEY)
        self.geonames = geonamescache.GeonamesCache()
        self.geolocator = Nominatim(user_agent="travel_around_the_world")
        
    def get_longitude_latitude_tuple(self, place_str):
        """This function is able to extract the longitude and latitude 
        only if place_str is a valid city or country. """
        location = self.geolocator.geocode(place_str)
        if location is not None:
            return (location.latitude, location.longitude)
        raise AttributeError("Unable to extract latitude and longitude of this location.")
    
    def find_places_given_place_type_and_radius(self, place, radius, type = ""):
        """The idea for this function is to find via textsearch all of the places of a certain
        type around a given place (given city and radius). From the information we will extract 
        only the valid ones (with rating), we will keep the information about the place_id, formatted_address,
        geometry/location, rating, user_ratings_total, type and name. If type is not specified, then the 
        query will be only for a specified place (country, province or city)."""
        # Basic url for text search via Google Maps API - Places.
        URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        # When the city is specified in the query, it overrides the location parameter.
        # If we pass the desired longitude and latitude, it is possible for them to be overriden by
        # other factors such as nearby location.
        if type == '':
            query = place
        else:
            query = type + ' in ' + place
        parameters = {'query':query, 'radius': radius, 'key':API_KEY}
        curr_request = requests.get(url = URL, params = parameters)
        data = curr_request.json()
        # data['results'][index]['place_id']
        # data['results'][index]['formatted_address']
        # data['results'][index]['geometry']['location']['lat']
        # data['results'][index]['geometry']['location']['lng']
        # data['results'][index]['types']
        # data['results'][index]['rating']
        # data['results'][index]['user_ratings_total']
        # data['results'][index]['name']
        
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
        