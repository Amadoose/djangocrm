from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# This file defines the views for the 'website' app in the DCRM project.

# Create your views here.

def home(request):
    """
    Render the home page of the DCRM website.
    This view handles requests to the root URL and returns the home page template.
    """
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Datos correctos, bienvenido!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    # Always return a response
    return render(request, 'home.html', {})


def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('home')

def register_user(request):
    """
    Render the registration page for new users.
    This view handles requests to the registration URL and returns the registration template.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Here you would typically save the user to the database
        messages.success(request, 'Usuario registrado correctamente.')
        return redirect('home')
    
    return render(request, 'register.html', {})