from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import DreamDestinationsList

class MainPagesViews:
    @login_required(login_url='/login/')
    def home_page(request):
        """Welcome page."""
        return render(request, 'home_page.html')

    @login_required(login_url='/login/')
    def dream_destinations_view(request):
        """Dream destinations page."""
        context = {
            'dream_destination_lists': DreamDestinationsList.objects.filter(owner=request.user)
        }
        return render(request, 'dream_list.html', context)

    @login_required(login_url='/login/')
    def logout_view(request):
        """
        Logout view. Login is required. 
        Redirects to the login page. 
        """
        logout(request)
        return redirect("/login/")