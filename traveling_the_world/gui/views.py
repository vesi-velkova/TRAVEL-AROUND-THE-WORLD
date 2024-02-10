from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import DreamDestinationsList

@login_required(login_url='/login/')
def index(request):
    """Welcome page."""
    context = {
        'dream_destination_lists': DreamDestinationsList.objects.filter(owner=request.user)
    }
    return render(request, 'index.html', context)

@login_required(login_url='/login/')
def logout_view(request):
    """
    Logout view. Login is required. 
    Redirects to the login page. 
    """
    logout(request)
    return redirect("/login/")