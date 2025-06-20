from utils.decorators import auth_required
from django.urls import path
from . import views
# This file defines the URL patterns for the 'website' app in the DCRM project.

urlpatterns = [
    # AUTHENTICATE URLS
    path('', auth_required(views.home_optimized), name='home'),      
    path('clients/', auth_required(views.c_list), name='clients'),     
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'),    
    ### QUOTE
    path('api/search_clients/', auth_required(views.search_clients_api), name='search_clients_api'),
    path('api/search_agents/', auth_required(views.search_agents_api), name='search_agents_api'),    
    path('api/create-folio/', auth_required(views.crear_folio_api), name='crear_folio_api'),
    path('folio_detail/<int:folio_id>/', auth_required(views.folio_detail), name='folio_detail'),
    path('folio_detail/<int:folio_id>/update_comments/', auth_required(views.update_folio_comments), name='update_folio_comments'),
    path('folio_detail/<int:folio_id>/update_budget/', auth_required(views.update_folio_budget_form), name='update_folio_budget_form'),
    path('folio_detail/<int:folio_id>/toggle_status/', auth_required(views.update_folio_status), name='update_folio_status'),
    path('folios/', auth_required(views.folios_list), name='folios_list'),
    
    ### CLIENT URLS      
    path('clients/', auth_required(views.c_list), name='clients'),     
    path('clients/new/', auth_required( views.new_client), name='new_client'),
    path('clients/<int:pk>/', auth_required(views.client_detail), name='client_detail'), # Detail view
    path('clients/update_client/<int:pk>/', auth_required(views.update_client), name='update_client'),
    ### USER URLS
    path('users/', auth_required(views.users), name='users'),    
    path('users/new/', auth_required(views.new_user), name='new_user'),
    path('users/<int:pk>/', auth_required(views.user_detail), name='user_detail'),
    path('users/update_user/<int:pk>/', auth_required(views.update_user), name='update_user'),
    ### SUUPLIERS URLS
    path('suppliers/', auth_required(views.suppliers), name='suppliers'), 
    # API endpoints for each service type
    path('suppliers/api/<str:service_type>/data/', auth_required(views.get_service_data), name='get_service_data'),
    path('suppliers/api/<str:service_type>/update/', auth_required(views.update_service_data), name='update_service_data'),
    path('suppliers/api/<str:service_type>/delete/<int:record_id>/', auth_required(views.delete_service_record), name='delete_service_record'),
    path('suppliers/api/<str:service_type>/choices/', auth_required(views.get_field_choices), name='get_field_choices'),
    path('suppliers/<str:section>/', auth_required(views.suppliers_section), name='suppliers_section'),     
    ### DIVISA URL
    path('divisa/', auth_required(views.divisa), name='divisa'), 
    ### WIP
    path('quote/', auth_required(views.quote), name='quote'),   
    path('reports/', auth_required(views.reports), name='reports'),  
    path('administration/', auth_required(views.administration), name='administration'),  
] 

