from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='/login/')
def index(request):
    """Welcome page."""
    return render(request, 'index.html')

def logout_view(request):
    """
    Logout view. Login is required. 
    Redirects to the login page. 
    """
    #print(request.user)
    logout(request)
    #print(request.user)
    return redirect("/login/")