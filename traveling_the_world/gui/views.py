from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import DreamDestinationsList
from django.http import HttpResponseNotFound

class MainPagesViews:
    @login_required(login_url='/login/')
    def home_page(request):
        """Welcome page."""
        return render(request, 'home_page.html')

    @login_required(login_url='/login/')
    def dream_destinations_view(request):
        """Dream destinations page."""
        try:
            destination_list = DreamDestinationsList.objects.filter(owner=request.user)
        except (KeyError, DreamDestinationsList.DoesNotExist):
            return HttpResponseNotFound('Invalid link. No dream destinations.')
        context = {
            'name': destination_list.values().get()['dream_destinations_list'],
            'items': destination_list.get().items.all()
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