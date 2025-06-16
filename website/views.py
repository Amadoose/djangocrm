from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ClienteForm
import random, json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError, transaction, models
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from .models import Cliente, Hotel, Airline, Activity, Operator, Transport

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
    

# # # # # # # #
# CLIENT VIEWS #
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
# USER VIEWS #
# # # #  #######
def users(request):  
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})

def new_user(request): 
    images = [
        'img/wintoon3.jpg',
        'img/WIPToon.jpg',
        'img/wiptoon2.jpg',
    ]
    selected_image = random.choice(images)
    return render(request, 'users/user_form.html', {'selected_image': selected_image})

def user_detail(request, pk):
    user = get_object_or_404(user, pk=pk)
    return render(request, 'users/users_detail.html', {'user': user})

def update_user(request, pk):
    user = get_object_or_404(user, pk=pk)
    return render(request, 'clients/user_form.html')

# # # # # # # #
# SUPPLIERS VIEWS #
# # # #  #######

def suppliers(request):
    """Main suppliers page view"""
    context = {
        'hotels': Hotel.objects.all(),
        'airlines': Airline.objects.all(),
        'activities': Activity.objects.all(),
        'operators': Operator.objects.all(),
        'transports': Transport.objects.all(),
    }
    return render(request, 'suppliers/suppliers.html', context)

def suppliers_section(request, section):
    """View for specific supplier sections"""
    return render_suppliers_view(request, section)

def render_suppliers_view(request, active_section=None):
    """Shared view logic"""
    valid_sections = {
        'hotels': Hotel.objects.all(),
        'airlines': Airline.objects.all(),
        'activities': Activity.objects.all(),
        'operators': Operator.objects.all(),
        'transports': Transport.objects.all()
    }
    
    context = {
        'active_section': active_section,
        **valid_sections
    }
    
    if active_section and active_section not in valid_sections:
        return redirect('suppliers')
        
    return render(request, 'suppliers/suppliers.html', context)


@csrf_exempt
@require_http_methods(["GET"])
def get_service_data(request, service_type):
    """Get data for a specific service type"""
    try:
        if service_type == 'hotels':
            data = list(Hotel.objects.values())
        elif service_type == 'airlines':
            data = list(Airline.objects.values())
        elif service_type == 'activities':
            data = list(Activity.objects.values())
        elif service_type == 'operators':
            data = list(Operator.objects.values())
        elif service_type == 'transports':
            data = list(Transport.objects.values())
        else:
            return JsonResponse({'error': 'Invalid service type'}, status=400)
        
        return JsonResponse({'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def clean_field_value(field, value, model_class):
    """Clean and convert field values based on field type"""
    if value == '' or value is None:
        if field.null:
            return None
        elif field.blank and isinstance(field, (models.CharField, models.TextField)):
            return ''
        elif hasattr(field, 'default') and field.default != models.NOT_PROVIDED:
            return field.default
        else:
            return value
    
    # Handle specific field types
    if isinstance(field, models.DecimalField):
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise ValidationError(f'{field.name} must be a valid decimal number')
    
    elif isinstance(field, models.IntegerField):
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValidationError(f'{field.name} must be a valid integer')
    
    elif isinstance(field, models.BooleanField):
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)
    
    elif isinstance(field, models.EmailField):
        if value and '@' not in str(value):
            raise ValidationError(f'{field.name} must be a valid email address')
        return value
    
    elif isinstance(field, models.URLField):
        if value and not (str(value).startswith('http://') or str(value).startswith('https://')):
            # Add http:// if no protocol specified
            return f'http://{value}'
        return value
    
    elif hasattr(field, 'choices') and field.choices:
        # Validate choice fields
        valid_choices = [choice[0] for choice in field.choices]
        if value not in valid_choices:
            raise ValidationError(f'{field.name} must be one of: {", ".join(valid_choices)}')
        return value
    
    return value

@csrf_exempt
@require_http_methods(["POST"])
def update_service_data(request, service_type):
    """Update or create service data with proper field validation"""
    try:
        # Parse JSON data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
        # Get the appropriate model
        model_map = {
            'hotels': Hotel,
            'airlines': Airline,
            'activities': Activity,
            'operators': Operator,
            'transports': Transport,
        }
       
        if service_type not in model_map:
            return JsonResponse({'error': 'Invalid service type'}, status=400)
       
        Model = model_map[service_type]
        
        # Fields that should never be updated via this endpoint
        protected_fields = ['id', 'created_by', 'created_at', 'updated_at', 'modified_by']
        
        # Clean the data with proper field validation
        cleaned_data = {}
        for key, value in data.items():
            if key not in protected_fields:
                try:
                    field = Model._meta.get_field(key)
                    cleaned_data[key] = clean_field_value(field, value, Model)
                except Exception as field_error:
                    # If field doesn't exist or has validation error, skip it or return error
                    if hasattr(Model, key):  # Field exists but has validation error
                        return JsonResponse({'error': f'Error in field {key}: {str(field_error)}'}, status=400)
                    # Field doesn't exist, just skip it
                    continue
        
        # Use database transaction for data integrity
        with transaction.atomic():
            if 'id' in data and data['id']:
                # Update existing record
                try:
                    instance = get_object_or_404(Model, id=data['id'])
                    
                    # Update fields
                    for key, value in cleaned_data.items():
                        if hasattr(instance, key):
                            # Special handling for unique fields
                            field = Model._meta.get_field(key)
                            if getattr(field, 'unique', False) and value:
                                # Check for uniqueness (excluding current instance)
                                if Model.objects.filter(**{key: value}).exclude(id=instance.id).exists():
                                    return JsonResponse({'error': f'{key.replace("_", " ").title()} "{value}" already exists'}, status=400)
                            
                            setattr(instance, key, value)
                    
                    # Validate the instance before saving
                    instance.full_clean()
                    instance.save()
                    
                    action = 'updated'
                    
                except ValidationError as e:
                    error_messages = []
                    if hasattr(e, 'message_dict'):
                        for field, messages in e.message_dict.items():
                            error_messages.extend([f'{field}: {msg}' for msg in messages])
                    else:
                        error_messages.append(str(e))
                    return JsonResponse({'error': f'Validation error: {"; ".join(error_messages)}'}, status=400)
                
            else:
                # Create new record
                try:
                    # Create instance without saving to validate first
                    instance = Model(**cleaned_data)
                    instance.full_clean()  # Validate before saving
                    instance.save()
                    
                    action = 'created'
                    
                except ValidationError as e:
                    error_messages = []
                    if hasattr(e, 'message_dict'):
                        for field, messages in e.message_dict.items():
                            error_messages.extend([f'{field}: {msg}' for msg in messages])
                    else:
                        error_messages.append(str(e))
                    return JsonResponse({'error': f'Validation error: {"; ".join(error_messages)}'}, status=400)
       
        return JsonResponse({
            'success': True, 
            'id': instance.id,
            'action': action,
            'message': f'{service_type.capitalize()} {action} successfully'
        })
        
    except IntegrityError as e:
        return JsonResponse({'error': 'Database constraint violation. Please check for duplicate values.'}, status=400)
    
    except Exception as e:
        # Add more detailed error logging for debugging
        import traceback
        print(f"Unexpected error in update_service_data: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_service_record(request, service_type, record_id):
    """Delete a service record"""
    try:
        model_map = {
            'hotels': Hotel,
            'airlines': Airline,
            'activities': Activity,
            'operators': Operator,
            'transports': Transport,
        }
        
        if service_type not in model_map:
            return JsonResponse({'error': 'Invalid service type'}, status=400)
        
        Model = model_map[service_type]
        instance = get_object_or_404(Model, id=record_id)
        instance.delete()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Helper function to get field choices for frontend
@csrf_exempt
@require_http_methods(["GET"])
def get_field_choices(request, service_type):
    """Get choices for choice fields to populate dropdowns in frontend"""
    try:
        model_map = {
            'hotels': Hotel,
            'airlines': Airline,
            'activities': Activity,
            'operators': Operator,
            'transports': Transport,
        }
        
        if service_type not in model_map:
            return JsonResponse({'error': 'Invalid service type'}, status=400)
        
        Model = model_map[service_type]
        choices = {}
        
        # Get all choice fields
        for field in Model._meta.fields:
            if hasattr(field, 'choices') and field.choices:
                choices[field.name] = list(field.choices)
        
        return JsonResponse({'choices': choices})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)    

# # # # # # # #
# OTHERS
# # # #  #######

def divisa(request):
    return render(request, 'other/divisa.html')   

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