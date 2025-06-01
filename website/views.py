from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record  

# This file defines the views for the 'website' app in the DCRM project.

# Create your views here.

def home(request):
    """
    Render the home page of the DCRM website.
    This view handles requests to the root URL and returns the home page template.
    """
    records = Record.objects.all()  # Fetch all records from the database
    
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
    return render(request, 'home.html', {'records': records})


def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión.')
    return redirect('home')

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
            return redirect('home')
    else:
        form = SignUpForm()            
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})


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
        return redirect('home')
    
def delete_record(request, pk): 
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para eliminar un registro.')
        return redirect('home')
    
    record = Record.objects.get(id=pk)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Registro eliminado correctamente.')
        return redirect('home')
    
    # Si es GET, muestra la página de confirmación
    return render(request, 'confirm_delete.html', {'record': record})

def add_record(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para agregar un registro.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, 'Registro agregado correctamente.')
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
        return redirect('home')        


