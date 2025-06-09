from django.urls import path
from . import views
# This file defines the URL patterns for the 'website' app in the DCRM project.

urlpatterns = [
    # AUTHENTICATE URLS
    # path('home/', views.home, name='home'),      
    path('', views.users, name='users'),     
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'),    

    ### CUSTOMER URLS      
    path('customers/list/', views.c_list, name='customers'),     
    path('customers/add_customer/', views.add_customer, name='add_customer'),
    # Detail view
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    # Edit view
    path('customers/customer_edit/<int:pk>/', views.customer_edit, name='customer_edit'),

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

