from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home_page), # Map empty url to the Welcome view.
    path('login/', auth_views.LoginView.as_view()), # Add login url.
    path('logout/', views.logout_view), # Add logout url.
    path('dream_destinations/', views.dream_destinations_view), # Add dream destinations url.
    path('dream_destinations/details/', views.detailed_page),
    path('dream_destinations/remove_item/', views.remove_item),
    path('dream_destinations/add_item/', views.add_item),
    path('register/', views.register),
    path('destination/', views.find_destination_view),
]
