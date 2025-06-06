from django.urls import path
from . import views
# This file defines the URL patterns for the 'website' app in the DCRM project.

urlpatterns = [
    # path('home/', views.home, name='home'),      
    path('', views.login_user, name='login'),     
    path('logout/', views.logout_user, name='logout'),     
    path('register/', views.register_user, name='register'),  
    path('record/<int:pk>', views.customer_record, name='record'),  
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),              
    path('update_record/<int:pk>', views.update_record, name='update_record'), 
    path('add_record/', views.add_record, name='add_record'), 
    path('quote/', views.quote, name='quote'),   
    path('customers/', views.customers, name='customers'),  
    path('users/', views.users, name='users'),  
    path('reports/', views.reports, name='reports'),  
    path('administration/', views.administration, name='administration'),  
] 

