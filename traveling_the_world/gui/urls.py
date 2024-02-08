from django.urls import path

from . import views

urlpatterns = [
    path('', views.index), # Map empty url to the Welcome view.
]