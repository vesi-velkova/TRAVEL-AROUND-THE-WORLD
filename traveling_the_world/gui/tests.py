from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views

from . import models
from . import views
from . import forms

class TestViews(TestCase):
    REDIRECT_STATUS_CODE = 302
    SUCCESSFUL_STATUS_CODE = 200
    NOT_FOUND_STATUS_CODE = 404
    PASSWORD = 'pass1234'

    def setUp(self):
        """Prepare the test class."""
        self.client = Client()
        self.TEST_USER = User.objects.create_user(username = 'test_user',
                                                  password = self.PASSWORD, first_name = 'Testing')

    def test_home_page_view_not_loged_in(self):
        """Test when the client is trying to 
        access the home page before logining in."""
        url = reverse(views.home_page)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.REDIRECT_STATUS_CODE)

    def test_home_page_view_loged_in(self):
        """Test the home page when the client is 
        trying to access it after successful login."""
        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.home_page)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.SUCCESSFUL_STATUS_CODE)
        self.assertTemplateUsed(response, 'home_page.html')
        self.assertEqual(response.context['username'], self.TEST_USER.first_name)

    def test_dream_destinations_view_not_loged_in(self):
        """Test when the client is trying to access the 
        dream destinations tab before logining in."""
        url = reverse(views.dream_destinations_view)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.REDIRECT_STATUS_CODE)

    def test_dream_destinations_list_does_not_exist(self):
        """Test when the user doesn't have list with dream destinations."""
        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.dream_destinations_view)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.NOT_FOUND_STATUS_CODE)

    def test_dream_destinations_list_empty(self):
        """Test when the user has an empty list with dream destinations."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')
        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.dream_destinations_view)
        response = self.client.get(url)
        # Here we expect that the places.py functions work correctly.
        URL = 'https://lh3.googleusercontent.com/places/ANXAkqF8-HtmrqT45pxsKvU1eiKJxakzuXBgu6p1-XDeaOBxHF9tvUD1T-bcrwhME7hU-0nBh6pjLLerYHlgmk7cIOhPJC-iuz32kt0=s1600-w3024'

        self.assertEqual(response.status_code, self.SUCCESSFUL_STATUS_CODE)
        self.assertTemplateUsed(response, 'dream_list.html')
        self.assertIn(URL, response.content.decode())
        self.assertIn('name', response.context)
        self.assertIn('items', response.context)
        self.assertIn('photo', response.context)

    def test_dream_destinations_list_valid_destination(self):
        """Test when the client has at least one valid 
        destination in the dream destinations list."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')
        destination = models.Destination.objects.create(destination_name = 'Amsterdam',
                                                        country = 'Netherlands',
                                                        list_name = destination_list)

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.dream_destinations_view)
        response = self.client.get(url)

        # Here we expect that the places.py functions work correctly.
        URL = 'https://lh3.googleusercontent.com/places/ANXAkqFE6c9SV-XK_PtONP-tY-QPc5wxVDvnXXC4bR260GF-WRMBrmWICyUzhqoHSEq7mjuJ33CBu5Z30WIU5tpZC9Hb9iYwvG6q1IE=s1600-w4000'
        self.assertEqual(response.status_code, self.SUCCESSFUL_STATUS_CODE)
        self.assertTemplateUsed(response, 'dream_list.html')
        self.assertIn(URL, response.content.decode())
        self.assertIn('name', response.context)
        self.assertIn('items', response.context)
        self.assertIn('photo', response.context)

    def test_dream_destinations_list_invalid_destination(self):
        """Test when the client has only invalid 
        destination in the dream destinations list."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')
        destination = models.Destination.objects.create(destination_name = 'Invalid Destination',
                                                        country = 'Bulgaria',
                                                        list_name = destination_list)

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.dream_destinations_view)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.NOT_FOUND_STATUS_CODE)

    def test_dream_destinations_list_no_photo_destination(self):
        """Test when the client has a valid dream 
        destination in the list, but there is no photo for it."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')
        destination = models.Destination.objects.create(destination_name = 'Hungary',
                                                        country = 'Hungary',
                                                        list_name = destination_list)

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.dream_destinations_view)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.SUCCESSFUL_STATUS_CODE)
        self.assertTemplateUsed(response, 'dream_list.html')
        self.assertNotIn('photo', response.context)
        self.assertIn('name', response.context)
        self.assertIn('items', response.context)

    def test_find_destination_view_not_logged_in(self):
        """Test when the client is trying to access the 
        destination tab before logining in."""
        url = reverse(views.find_destination_view)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.REDIRECT_STATUS_CODE)

    def test_find_destination_view_list_does_not_exist(self):
        """Test when the user doesn't have list with destinations."""
        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.find_destination_view)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.NOT_FOUND_STATUS_CODE)

    def test_find_destination_view_list_valid_country(self):
        """Test when the client has at least one valid 
        country in the countries list."""
        curr_countries_list = models.CountryList.objects.create(owner = self.TEST_USER,
                                                                countries_in_the_world = 'Test List')
        country = models.Country.objects.create(name = 'Netherlands', cities_to_visit = 30,
                                                visited = True, countries_list = curr_countries_list)

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.find_destination_view)
        response = self.client.get(url)

        # Here we expect that the places.py functions work correctly.
        # We expect a background photo of the capital city.
        # Netherlands will be the most visited country, as it is the only one.
        URL = 'https://lh3.googleusercontent.com/places/ANXAkqFE6c9SV-XK_PtONP-tY-QPc5wxVDvnXXC4bR260GF-WRMBrmWICyUzhqoHSEq7mjuJ33CBu5Z30WIU5tpZC9Hb9iYwvG6q1IE=s1600-w4000'
        self.assertEqual(response.status_code, self.SUCCESSFUL_STATUS_CODE)
        self.assertTemplateUsed(response, 'destination.html')
        self.assertIn(URL, response.content.decode())

    # Side note: there is a function validating the
    # countries, before ading them to the page and db.
    # Therefore, it is impossible to have invalid country.
    # I can not find a capital city without photos on Google
    # Maps, so the photos exception handling is a precaution,
    # but not likely to happen at all.

    def test_detailed_page_view_not_loged_in(self):
        """Test when the client is trying to access the
        detailed page of a dream destination before logining in."""
        url = reverse(views.detailed_page)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.REDIRECT_STATUS_CODE)

    def test_detailed_page_view_id_does_not_exist(self):
        """Test when destination with this id doesn't exist."""
        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.detailed_page) + '?id=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.NOT_FOUND_STATUS_CODE)

    def test_detailed_page_view_valid_destination(self):
        """Test when the client has at least one valid
        destination in the dream destinations list and
        we are searching for detailed information about it."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')
        destination = models.Destination.objects.create(destination_name = 'Amsterdam',
                                                        country = 'Netherlands',
                                                        list_name = destination_list)

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.detailed_page) + f'?id={destination.pk}'
        response = self.client.get(url)

        # Here we expect that the places.py functions work correctly.
        URL = 'https://lh3.googleusercontent.com/places/ANXAkqFE6c9SV-XK_PtONP-tY-QPc5wxVDvnXXC4bR260GF-WRMBrmWICyUzhqoHSEq7mjuJ33CBu5Z30WIU5tpZC9Hb9iYwvG6q1IE=s1600-w4000'
        self.assertEqual(response.status_code, self.SUCCESSFUL_STATUS_CODE)
        self.assertTemplateUsed(response, 'details.html')
        self.assertIn(URL, response.content.decode())
        detailed_info_keys = ['name', 'subregion', 'region', 'capital', 'currencies',
                           'destination_name', 'languages','population', 'wiki', 'photo']
        for key in detailed_info_keys:
            self.assertIn(key, response.context)

    def test_detailed_page_view_invalid_destination(self):
        """Test getting detailed informatio when the client
        has only invalid destination in the dream destinations list."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')
        destination = models.Destination.objects.create(destination_name = 'Invalid Destination',
                                                        country = 'Bulgaria',
                                                        list_name = destination_list)

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.detailed_page) + f'?id={destination.pk}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, self.NOT_FOUND_STATUS_CODE)

    def test_detailed_page_view_no_photo_destination(self):
        """Test when the client has a valid dream 
        destination in the list, but there is no photo for it. 
        Take details for this destination."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')
        destination = models.Destination.objects.create(destination_name = 'Hungary',
                                                        country = 'Hungary',
                                                        list_name = destination_list)

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.detailed_page) + f'?id={destination.pk}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.SUCCESSFUL_STATUS_CODE)
        self.assertTemplateUsed(response, 'details.html')
        self.assertNotIn('photo', response.context)
        detailed_info_keys = ['name', 'subregion', 'region', 'capital', 'currencies',
                           'destination_name', 'languages','population', 'wiki']
        for key in detailed_info_keys:
            self.assertIn(key, response.context)

    def test_remove_item_successfully(self):
        """Test when the client removes a destination
        from the dream destination list successfully."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')
        destination = models.Destination.objects.create(destination_name = 'Amsterdam',
                                                        country = 'Netherlands',
                                                        list_name = destination_list)

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.remove_item) + f'?id={destination.pk}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, self.SUCCESSFUL_STATUS_CODE)
        self.assertFalse(models.Destination.objects.filter(pk = destination.pk).exists())

    def test_remove_item_not_loged_in(self):
        """Test when the client is trying to 
        remove a destination before logining in."""
        url = reverse(views.remove_item)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.REDIRECT_STATUS_CODE)

    def test_remove_item_invalid_id(self):
        """Try to remove an item from the 
        dream destination list with invalid id."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')
        destination = models.Destination.objects.create(destination_name = 'Amsterdam',
                                                        country = 'Netherlands',
                                                        list_name = destination_list)

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.remove_item) + f'?id=777'
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.NOT_FOUND_STATUS_CODE)

    def test_remove_item_other_user(self):
        """Try to remove an item from the 
        dream destination list of another user."""
        other_user = User.objects.create_user(username = 'test_user_2',
                                            password = self.PASSWORD, first_name = 'Testing_2')
        destination_list = models.DreamDestinationsList.objects.create(owner = other_user,
                                                                    dream_destinations_list = 'Test List')
        destination = models.Destination.objects.create(destination_name = 'Amsterdam',
                                                        country = 'Netherlands',
                                                        list_name = destination_list)
        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.remove_item) + f'?id={destination.pk}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.NOT_FOUND_STATUS_CODE)

    def test_add_item_successfully(self):
        """Test when the client adds a destination
        to the dream destination list successfully."""
        destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')

        self.client.login(username = self.TEST_USER.username,
                          password = self.PASSWORD)
        url = reverse(views.add_item)
        response = self.client.post(url, {'destination_name': 'Amsterdam', 'country':'Netherlands'})

        self.assertEqual(response.status_code, self.REDIRECT_STATUS_CODE)
        self.assertTrue(models.Destination.objects.filter(destination_name = 'Amsterdam').exists())


class TestForms(TestCase):
    DEST_NAME_STR = 'Amsterdam'
    COUNTRY_STR = 'Netherlands'
    USERNAME = 'test_user'
    PASSWORD = 'burgas@01_usr'
    PASS_COMMON = 'test1234'
    PASS_DIGITS = '12345678'
    PASS_SHORT = 'test1'
    PASS_SIMILAR = 'test_user'
    NAME = 'Vesi'
    FAMILY_NAME = 'Testing'

    def setUp(self):
        self.TEST_USER = User.objects.create_user(username = 'test_user_base',
                                                  password = self.PASSWORD, first_name = 'Testing')
        self.destination_list = models.DreamDestinationsList.objects.create(owner = self.TEST_USER,
                                                                    dream_destinations_list = 'Test List')

    def test_destination_valid(self):
        fill_in_data = {
            'destination_name':self.DEST_NAME_STR,
            'country':self.COUNTRY_STR,
            'list_name':self.destination_list
        }
        form = forms.AddDestinationForm(fill_in_data)
        self.assertTrue(form.is_valid())

    def test_destination_missed_list(self):
        fill_in_data = {
            'destination_name':self.DEST_NAME_STR,
            'country':self.COUNTRY_STR,
        }
        form = forms.AddDestinationForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_destination_missed_dest_name(self):
        fill_in_data = {
            'country':self.COUNTRY_STR,
            'list_name':self.destination_list
        }
        form = forms.AddDestinationForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_destination_missing_country(self):
        fill_in_data = {
            'destination_name':self.DEST_NAME_STR,
            'list_name':self.destination_list
        }
        form = forms.AddDestinationForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_destination_country_name_too_long(self):
        fill_in_data = {
            'destination_name':self.DEST_NAME_STR,
            'country':'AlaBala'*8,
            'list_name':self.destination_list
        }
        form = forms.AddDestinationForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_registration_valid(self):
        fill_in_data = {
            'username':self.USERNAME,
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASSWORD,
            'password2':self.PASSWORD
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertTrue(form.is_valid())

    def test_registration_username_already_exists(self):
        fill_in_data = {
            'username':'test_user_base',
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASSWORD,
            'password2':self.PASSWORD
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_registration_password_too_common(self):
        fill_in_data = {
            'username':self.USERNAME,
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASS_COMMON,
            'password2':self.PASS_COMMON
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_registration_password_only_digits(self):
        fill_in_data = {
            'username':self.USERNAME,
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASS_DIGITS,
            'password2':self.PASS_DIGITS
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_registration_password_too_short(self):
        fill_in_data = {
            'username':self.USERNAME,
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASS_SHORT,
            'password2':self.PASS_SHORT
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_registration_pass_similar_to_username(self):
        fill_in_data = {
            'username':self.USERNAME,
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASS_SIMILAR,
            'password2':self.PASS_SIMILAR
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_registration_passwords_different(self):
        fill_in_data = {
            'username':self.USERNAME,
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASSWORD,
            'password2':'burgas@02_usr'
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_registration_password_missing_1(self):
        fill_in_data = {
            'username':self.USERNAME,
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password2':self.PASSWORD,
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_registration_password_missing_2(self):
        fill_in_data = {
            'username':self.USERNAME,
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASSWORD,
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertFalse(form.is_valid())

    def test_registration_first_name_missing(self):
        fill_in_data = {
            'username':self.USERNAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASSWORD,
            'password2':self.PASSWORD,
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertTrue(form.is_valid())

    def test_registration_last_name_missing(self):
        fill_in_data = {
            'username':self.USERNAME,
            'first_name':self.NAME,
            'password1':self.PASSWORD,
            'password2':self.PASSWORD,
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertTrue(form.is_valid())

    def test_registration_username_missing(self):
        fill_in_data = {
            'first_name':self.NAME,
            'last_name':self.FAMILY_NAME,
            'password1':self.PASSWORD,
            'password2':self.PASSWORD,
        }
        form = forms.RegisterUserForm(fill_in_data)
        self.assertFalse(form.is_valid())


class TestUrls(TestCase):

    def test_base_url(self):
        url = reverse(views.home_page)
        self.assertEqual(resolve(url).func, views.home_page)

    def test_dream_destinations_url(self):
        url = reverse(views.dream_destinations_view)
        self.assertEqual(resolve(url).func, views.dream_destinations_view)

    def test_destination_url(self):
        url = reverse(views.find_destination_view)
        self.assertEqual(resolve(url).func, views.find_destination_view)

    def test_details_url(self):
        url = reverse(views.detailed_page)
        self.assertEqual(resolve(url).func, views.detailed_page)

    def test_remove_item_url(self):
        url = reverse(views.remove_item)
        self.assertEqual(resolve(url).func, views.remove_item)

    def test_add_item_url(self):
        url = reverse(views.add_item)
        self.assertEqual(resolve(url).func, views.add_item)

    def test_register_url(self):
        url = reverse(views.register)
        self.assertEqual(resolve(url).func, views.register)

    def test_visit_item_url(self):
        url = reverse(views.visit_item_view)
        self.assertEqual(resolve(url).func, views.visit_item_view)

    def test_logout_url(self):
        url = reverse(views.logout_view)
        self.assertEqual(resolve(url).func, views.logout_view)