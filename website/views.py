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
from django.core.exceptions import ValidationError, PermissionDenied
from decimal import Decimal, InvalidOperation
from .models import Cliente, Hotel, Airline, Activity, Operator, Transport, Folio
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.urls import reverse
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from datetime import timedelta


# This file defines the views for the 'website' app in the DCRM project.
# User authentication views
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) 
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('home')
        else:
            messages.error(request, 'Datos incorrectos!')
            return redirect('login')

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


# HOME
# HOME
def home(request):
    """
    Home view showing folio statistics and user's folios
    Supports AJAX requests for live search
    """
    # Get current user's folios (or all if staff)
    if request.user.is_staff:
        folios_qs = Folio.objects.select_related('cliente', 'agente').all()
    else:
        folios_qs = Folio.objects.select_related('cliente', 'agente').filter(agente=request.user)
    
    # Calculate days open for each folio and add status
    folios_with_days = []
    for folio in folios_qs:
        days_open = (timezone.now().date() - folio.created_at.date()).days
        folio.days_open = days_open
        
        # Determine status based on days open
        if days_open <= 7:
            folio.status = 'hot'
        elif days_open <= 30:
            folio.status = 'lukewarm'
        else:
            folio.status = 'cold'
        
        folios_with_days.append(folio)
    
    # Filter by search
    search_query = request.GET.get('search', '')
    if search_query:
        folios_with_days = [
            f for f in folios_with_days 
            if (search_query.lower() in f.name.lower() or
                search_query.lower() in f.cliente.nombre.lower() or
                search_query.lower() in f.cliente.apellido_paterno.lower() or
                search_query.lower() in str(f.id))
        ]
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter and status_filter != 'all':
        folios_with_days = [f for f in folios_with_days if f.status == status_filter]
    
    # Sort by current_sort parameter
    current_sort = request.GET.get('sort', '-created_at')
    
    # Handle sorting
    reverse = current_sort.startswith('-')
    sort_field = current_sort.lstrip('-')
    
    if sort_field == 'id':
        folios_with_days.sort(key=lambda x: x.id, reverse=reverse)
    elif sort_field == 'cliente__nombre':
        folios_with_days.sort(key=lambda x: x.cliente.nombre, reverse=reverse)
    elif sort_field == 'tipo_viaje':
        folios_with_days.sort(key=lambda x: x.tipo_viaje, reverse=reverse)
    elif sort_field == 'created_at':
        folios_with_days.sort(key=lambda x: x.created_at, reverse=reverse)
    elif sort_field == 'budget':
        folios_with_days.sort(key=lambda x: x.budget or 0, reverse=reverse)
    else:
        # Default sort by created_at descending
        folios_with_days.sort(key=lambda x: x.created_at, reverse=True)
    
    # Calculate statistics
    total_folios = len(folios_with_days)
    open_folios_count = len([f for f in folios_with_days if f.is_active])
    cold_folios_count = len([f for f in folios_with_days if f.status == 'cold' and f.is_active])
    
    # Calculate total budget (only active folios with budget)
    total_budget = sum(f.budget for f in folios_with_days 
                      if f.is_active and f.budget and f.budget > 0)
    
    # Recent activity (folios updated in last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_activity_count = len([f for f in folios_with_days 
                                if f.updated_at >= seven_days_ago])
    
    # Pagination
    paginator = Paginator(folios_with_days, 20)  # Show 20 folios per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'folios': page_obj,
        'total_folios': total_folios,
        'open_folios_count': open_folios_count,
        'cold_folios_count': cold_folios_count,
        'total_budget': total_budget,
        'recent_activity_count': recent_activity_count,
        'current_search': search_query,
        'status_filter': status_filter,
        'current_sort': current_sort,
        'title': 'Home'
    }
    
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # For AJAX requests, return the full template (the JS will extract what it needs)
        return render(request, 'home.html', context)
    
    return render(request, 'home.html', context)

# Alternative approach using database queries (more efficient for large datasets)
@login_required 
def home_optimized(request):
    """
    Optimized home view using database aggregations
    """
    # Get current user's folios
    if request.user.is_staff:
        base_qs = Folio.objects.select_related('cliente', 'agente')
    else:
        base_qs = Folio.objects.select_related('cliente', 'agente').filter(agente=request.user)
    
    # Filter by search
    search_query = request.GET.get('search', '')
    if search_query:
        base_qs = base_qs.filter(
            Q(name__icontains=search_query) |
            Q(cliente__nombre__icontains=search_query) |
            Q(cliente__apellido_paterno__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    # Calculate date thresholds
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)
    
    # Filter by status (if specified)
    status_filter = request.GET.get('status', '')
    if status_filter == 'hot':
        base_qs = base_qs.filter(created_at__gte=seven_days_ago)
    elif status_filter == 'lukewarm':
        base_qs = base_qs.filter(
            created_at__lt=seven_days_ago,
            created_at__gte=thirty_days_ago
        )
    elif status_filter == 'cold':
        base_qs = base_qs.filter(created_at__lt=thirty_days_ago)
    
    # Sorting
    current_sort = request.GET.get('sort', '-created_at')
    valid_sorts = {
        'id', '-id',
        'cliente__nombre', '-cliente__nombre', 
        'tipo_viaje', '-tipo_viaje',
        'created_at', '-created_at',
        'budget', '-budget'
    }
    
    if current_sort in valid_sorts:
        folios_qs = base_qs.order_by(current_sort)
    else:
        folios_qs = base_qs.order_by('-created_at')
    
    # Add computed fields for template
    folios_list = []
    for folio in folios_qs:
        days_open = (now.date() - folio.created_at.date()).days
        folio.days_open = days_open
        
        if days_open <= 7:
            folio.status = 'hot'
        elif days_open <= 30:
            folio.status = 'lukewarm'
        else:
            folio.status = 'cold'
        
        folios_list.append(folio)
    
    # Calculate statistics using database aggregations
    stats_qs = base_qs.aggregate(
        total_folios=Count('id'),
        open_folios=Count('id', filter=Q(is_active=True)),
        cold_folios=Count('id', filter=Q(is_active=True, created_at__lt=thirty_days_ago)),
        total_budget=Sum('budget', filter=Q(is_active=True, budget__gt=0)),
        recent_activity=Count('id', filter=Q(updated_at__gte=seven_days_ago))
    )
    
    # Pagination
    paginator = Paginator(folios_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'folios': page_obj,
        'total_folios': stats_qs['total_folios'] or 0,
        'open_folios_count': stats_qs['open_folios'] or 0,
        'cold_folios_count': stats_qs['cold_folios'] or 0,
        'total_budget': stats_qs['total_budget'] or 0,
        'recent_activity_count': stats_qs['recent_activity'] or 0,
        'current_search': search_query,
        'status_filter': status_filter,
        'current_sort': current_sort,
        'title': 'Home'
    }
    
    return render(request, 'home.html', context)

# QUOTE_FOLIO
# QUOTE_FOLIO
# QUOTE_FOLIO

def search_clients_api(request):
    """API endpoint for Tom Select client search. Returns ALL matching clients."""
    search_term = request.GET.get('q', '')

    # Start with all clients from the table
    clientes_qs = Cliente.objects.all()

    # If the user is searching, filter the queryset
    if search_term:
        clientes_qs = clientes_qs.filter(
            Q(id__icontains=search_term) |
            Q(nombre__icontains=search_term) | 
            Q(apellido_paterno__icontains=search_term) |
            Q(email__icontains=search_term)
        )
    
    # Order the final list by ID
    clientes_qs = clientes_qs.order_by('id')

    # Convert the entire queryset to a list of dictionaries
    # NO PAGINATION IS USED HERE
    results = []
    for cliente in clientes_qs:
        results.append({
            "id": cliente.id,
            "text": f"{cliente.nombre} {cliente.apellido_paterno}",
            "nombre": cliente.nombre,
            "apellido_paterno": cliente.apellido_paterno,
            "email": cliente.email
        })
    
    return JsonResponse({'results': results})

def search_agents_api(request):
    """API endpoint for Tom Select agent search. Returns ALL matching agents."""
    search_term = request.GET.get('q', '')

    # Start with all users from the table
    agentes_qs = User.objects.all()

    # If the user is searching, filter the queryset
    if search_term:
        agentes_qs = agentes_qs.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(username__icontains=search_term)
        )
    
    # Order the final list by ID
    agentes_qs = agentes_qs.order_by('id')
    
    # Convert the entire queryset to a list of dictionaries
    # NO PAGINATION IS USED HERE
    results = []
    for agente in agentes_qs:
        results.append({
            "id": agente.id,
            "text": f"{agente.first_name} {agente.last_name} ({agente.username})",
            "first_name": agente.first_name,
            "last_name": agente.last_name,
            "username": agente.username
        })

    return JsonResponse({'results': results})

def crear_folio_api(request):
    """View to create a new folio"""
    if request.method == 'POST':        
        try:
            cliente_id = request.POST.get('cliente')
            agente_id = request.POST.get('agente')
            tipo_viaje = request.POST.get('tipo_viaje')
            name = request.POST.get('name')
            
            # Validate required fields
            if not all([name, cliente_id, agente_id, tipo_viaje]):
                return JsonResponse({'success': False, 'error': 'Todos los campos son requeridos.'}, status=400)
            
            # Get the objects
            cliente = Cliente.objects.get(id=cliente_id)
            agente = User.objects.get(id=agente_id)
            
            # Create the folio
            folio = Folio.objects.create(
                name=name,
                cliente=cliente,
                agente=agente,
                tipo_viaje=tipo_viaje
            )
            
            messages.success(request, f'Folio #{folio.id} creado exitosamente.')
            
            # Generate the URL for the new folio
            redirect_url = reverse('folio_detail', kwargs={'folio_id': folio.id})

            return JsonResponse({'success': True, 'redirect_url': redirect_url})

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'An exception occurred: {str(e)}'}, status=500)
    
    # If the request is NOT POST, return an error.
    return JsonResponse({'success': False, 'error': 'Invalid request method for this endpoint.'}, status=405)
    
    
def folio_detail(request, folio_id):
    """
    Display folio detail page with all information
    """
    folio = get_object_or_404(Folio, id=folio_id)
    
    # Check if user has permission to view this folio
    # You can add your own permission logic here
    # if not request.user.has_perm('view_folio', folio):
    #     messages.error(request, 'No tienes permisos para ver este folio.')
    #     return redirect('folios_list')
    
    context = {
        'folio': folio,
        'title': f'Folio #{folio.id} - {folio.name}',
    }
    
    return render(request, 'quote/folio_detail.html', context)


@require_http_methods(["POST"])
def update_folio_comments(request, folio_id):
    """
    AJAX endpoint to update folio comments
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    try:
        folio = get_object_or_404(Folio, id=folio_id)
        
        # Check permissions
        # if not request.user.has_perm('change_folio', folio):
        #     return JsonResponse({'success': False, 'error': 'Sin permisos'}, status=403)
        
        data = json.loads(request.body)
        comments = data.get('comments', '')
        
        # Update comments
        folio.comments = comments
        folio.save(update_fields=['comments', 'updated_at'])
        
        return JsonResponse({
            'success': True,
            'message': 'Comentarios guardados exitosamente',
            'updated_at': folio.updated_at.strftime('%d/%m/%Y %H:%M')
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_http_methods(["POST"])
def update_folio_budget_form(request, folio_id):
    folio = get_object_or_404(Folio, id=folio_id)
    
    if not request.user.has_perm('change_folio', folio):
        messages.error(request, 'No tienes permisos para modificar este folio.')       
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'No tienes permiso'}, status=403)
    
    budget_value = request.POST.get('budget', '0')               
    try:
        budget = Decimal(budget_value)
        if budget < 0:
            messages.error(request, 'El presupuesto no puede ser negativo.')
        else:
            old_budget = folio.budget
            folio.budget = budget
            folio.save(update_fields=['budget', 'updated_at'])
            messages.success(request, f'Presupuesto actualizado de ${old_budget:,.2f} a ${budget:,.2f}')
    except (InvalidOperation, ValueError):        
        messages.error(request, 'Formato de presupuesto inválido.')

     # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Budget updated successfully'})            
    
    return redirect('folio_detail', folio_id=folio.id)


def update_folio_status(request, folio_id):
    """
    Toggle folio active status
    """
    if request.method == 'POST':
        folio = get_object_or_404(Folio, id=folio_id)
        
        # Check permissions
        # if not request.user.has_perm('change_folio', folio):
        #     messages.error(request, 'No tienes permisos para modificar este folio.')
        #     return redirect('folio_detail', folio_id=folio.id)
        
        # Toggle status
        folio.is_active = not folio.is_active
        folio.save(update_fields=['is_active', 'updated_at'])
        
        status_text = "activado" if folio.is_active else "desactivado"
        messages.success(request, f'Folio #{folio.id} {status_text} exitosamente.')
        
        return redirect('folio_detail', folio_id=folio.id)
    
    return redirect('folio_detail', folio_id=folio_id)

# Optional: List view for folios

def folios_list(request):
    """
    List all folios with search and filter functionality
    """
    folios = Folio.objects.select_related('cliente', 'agente').all()
        
    # Add search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        folios = folios.filter(
            models.Q(name__icontains=search_query) |
            models.Q(cliente__nombre__icontains=search_query) |
            models.Q(cliente__apellido_paterno__icontains=search_query) |
            models.Q(agente__first_name__icontains=search_query) |
            models.Q(agente__last_name__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        folios = folios.filter(is_active=True)
    elif status_filter == 'inactive':
        folios = folios.filter(is_active=False)
    
    # Filter by celebration type
    tipo_filter = request.GET.get('tipo', '')
    if tipo_filter:
        folios = folios.filter(tipo_viaje=tipo_filter)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(folios, 20)  # Show 20 folios per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'tipo_filter': tipo_filter,
        'tipo_choices': Folio.TIPO_VIAJE_CHOICES,
        'title': 'Lista de Folios'
    }
    
    return render(request, 'quote/folios_list.html', context)



# # # # # # # #
# CLIENT VIEWS #
# # # #  #######

##customer index
def c_list(request):
    search_term = request.GET.get('search', '')
    filter_type = request.GET.get('filter', 'all')
    sort_column = request.GET.get('sort', '-id')
    
    # Validate sort column
    valid_columns = {
        'id', '-id', 
        'nombre', '-nombre',
        'apellido_paterno', '-apellido_paterno',
        'apellido_materno', '-apellido_materno',
        'email', '-email',
        'celular', '-celular',
        'nacionalidad', '-nacionalidad',
        'nivel_lealtad', '-nivel_lealtad'
    }
    
    if sort_column not in valid_columns:
        sort_column = '-id'
    
    client_list = Cliente.objects.all()
    
    if search_term:
        client_list = client_list.filter(
            Q(nombre__icontains=search_term) |
            Q(apellido_paterno__icontains=search_term) |
            Q(apellido_materno__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(celular__icontains=search_term)
        )
    
    if filter_type == 'recent':
        client_list = client_list.order_by('-id')[:100]
    else:
        client_list = client_list.order_by(sort_column)
        # if sort_column.lstrip('-') == 'id':
        #     client_list = client_list.order_by('id')
        # else:
        #     client_list = client_list.order_by(sort_column)
    
    paginator = Paginator(client_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'clients/list.html', {
        'clientes': page_obj,
        'current_sort': sort_column,
        'current_search': search_term,
        'current_filter': filter_type,
        'total_count': client_list.count(),
        'request': request  # Make request available for url_replace
    })

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
