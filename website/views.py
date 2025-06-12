from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ClienteForm, AddRecordForm
from .models import Record, Cliente
import random
from django.contrib.auth.models import User

# This file defines the views for the 'website' app in the DCRM project.

# Create your views here.


# User authentication views
# User authentication views
# User authentication views

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) 
            return redirect('users')
        else:
            return render(request, 'users.html', {'error': 'Invalid credentials, please try again.'})
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión.')
    return redirect('login')

# User creation view
# User creation view
# User creation view
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate the user after registration and log them in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Authenticate the user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Cuenta creada para {username}. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = SignUpForm()            
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

#REGISTRY CREATION VIEWS
#REGISTRY CREATION VIEWS
#REGISTRY CREATION VIEWS
def customer_record(request, pk):
    """
    Render the customer record page for a specific record identified by its primary key (pk).
    This view fetches the record from the database and displays its details.
    """
    if request.user.is_authenticated:
        # If the user is authenticated, they can view the record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        # If the user is not authenticated, redirect to the home page
        messages.success(request, 'Debes iniciar sesión para ver los registros.')
        return redirect('login')
    
def delete_record(request, pk): 
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para eliminar un registro.')
        return redirect('login')
    
    record = Record.objects.get(id=pk)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Registro eliminado correctamente.')
        return redirect('users')
    
    # Si es GET, muestra la página de confirmación
    return render(request, 'confirm_delete.html', {'record': record})

def add_record(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must log in to add a customer.')
        return redirect('login')
    
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, 'Correctly added.')
            return redirect('record', pk=record.id)  # Redirige al detalle del registro
    else:        
        form = AddRecordForm()    
    return render(request, 'add_record.html', {'form': form})

def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro actualizado correctamente.')
            return redirect('record', pk=record.id)
        return render(request, 'update_record.html', {'form': form, 'record': record})
    else:
        messages.error(request, 'Debes iniciar sesión para actualizar un registro.')
        return redirect('login')        
    

# # # # # # # #
# CUSTOMERS VIEWS #
# # # #  #######

##customer index
def c_list(request):
    # Query all Cliente objects from the DB
    clientes = Cliente.objects.all()
    return render(request, 'clients/list.html', {'clientes': clientes})

def new_client(request):
    # Handle form submission
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Save the data to the database
            return redirect('clients')  # Redirect after successful submission
    else:
        form = ClienteForm()  # Show a blank form for GET request
    return render(request, 'clients/client_form.html', {'form': form, 'is_update': False})

def client_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'clients/client_detail.html', {'cliente': cliente})

def update_client(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clients/client_form.html', {'form': form, 'is_update': True})


# # # # # # # #
# CUSTOMERS VIEWS #
# # # #  #######
def users(request):
    if not request.user.is_authenticated:
        return redirect('login')    
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})

#########
#WORK IN PROGRESS
###########

def quote(request):
    images = [
        'img/wintoon3.jpg',
        'img/WIPToon.jpg',
        'img/wiptoon2.jpg',
    ]
    selected_image = random.choice(images)
    return render(request, 'quote.html', {'selected_image': selected_image})

def reports(request):
    images = [
        'img/wintoon3.jpg',
        'img/WIPToon.jpg',
        'img/wiptoon2.jpg',
    ]
    selected_image = random.choice(images)
    return render(request, 'reports.html', {'selected_image': selected_image})

def administration(request):
    images = [
        'img/wintoon3.jpg',
        'img/WIPToon.jpg',
        'img/wiptoon2.jpg',
    ]
    selected_image = random.choice(images)
    return render(request, 'administration.html', {'selected_image': selected_image})