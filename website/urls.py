from utils.decorators import auth_required
from django.urls import path
from . import views
# This file defines the URL patterns for the 'website' app in the DCRM project.

urlpatterns = [
    # AUTHENTICATE URLS
    # path('home/', views.home, name='home'),      
    path('', views.c_list, name='clients'),     
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'),    

    ### CLIENT URLS      
    path('clients/', auth_required(views.c_list), name='clients'),     
    path('clients/new/', auth_required( views.new_client), name='new_client'),
    # Detail view
    path('clients/<int:pk>/', auth_required(views.client_detail), name='client_detail'),
    # Edit view
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
    # path('hotels/', auth_required(views.hotels_view), name='hotels'),
    # path('airlines/', auth_required(views.airlines_view), name='airlines'),
    # path('activities/', auth_required(views.activities_view), name='activities'),
    # path('operators/', auth_required(views.operators_view), name='operators'),
    # path('other_transport/', auth_required(views.transport_view), name='other_transport'),
    
    ### HOTEL
    ### AEROLINEAS
    ### ACTIVIDADES
    ### OPERADOR
    ### OTRO TRANSPORTE

    ### DIVISA URL
    path('divisa/', auth_required(views.divisa), name='divisa'), 


    ### functionality

    ### WIP
    path('quote/', auth_required(views.quote), name='quote'),   
    path('reports/', auth_required(views.reports), name='reports'),  
    path('administration/', auth_required(views.administration), name='administration'),  
] 

