from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home_page), # Map empty url to the Welcome view.
    path('login/', auth_views.LoginView.as_view()), # Add login url.
    path('dream_destinations/', views.dream_destinations_view), # Add url for the dream destinations page.
    path('destination/', views.find_destination_view), # Add url for the destinations page.
    path('dream_destinations/details/', views.detailed_page), # Add detailed page for each dream destination.
    path('remove_item/', views.remove_item), # Remove an item from the dream_destination list.
    path('dream_destinations/add_item/', views.add_item),
    path('register/', views.register), # Add registration url.
    path('visit_item/', views.visit_item_view),
    path('logout/', views.logout_view), # Add logout url.
]
