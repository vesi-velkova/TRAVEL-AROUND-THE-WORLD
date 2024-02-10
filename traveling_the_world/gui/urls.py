from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.MainPagesViews.home_page), # Map empty url to the Welcome view.
    path('login/', auth_views.LoginView.as_view()), # Add login url.
    path('logout/', views.MainPagesViews.logout_view), # Add logout url.
    path('dream_destinations/', views.MainPagesViews.dream_destinations_view), # Add dream destinations url.
]
