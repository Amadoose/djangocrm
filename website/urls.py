from django.urls import path
from . import views
# This file defines the URL patterns for the 'website' app in the DCRM project.

urlpatterns = [
    # AUTHENTICATE URLS
    # path('home/', views.home, name='home'),      
    path('', views.c_list, name='clients'),     
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'),    

    ### CUSTOMER URLS      
    path('clients/', views.c_list, name='clients'),     
    path('clients/new/', views.new_client, name='new_client'),
    # Detail view
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    # Edit view
    path('clients/update_client/<int:pk>/', views.update_client, name='update_client'),

    ### functionality
    path('users/', views.users, name='users'),
    path('register/', views.register_user, name='register'),  
    path('record/<int:pk>', views.customer_record, name='record'),  
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),              
    path('update_record/<int:pk>', views.update_record, name='update_record'), 
    path('add_record/', views.add_record, name='add_record'), 
    ### WIP
    path('quote/', views.quote, name='quote'),   
    path('reports/', views.reports, name='reports'),  
    path('administration/', views.administration, name='administration'),  
] 

