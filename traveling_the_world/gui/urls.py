from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index), # Map empty url to the Welcome view.
    path('login', auth_views.LoginView.as_view()) # Add login url.
]