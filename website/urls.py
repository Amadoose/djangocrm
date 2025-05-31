from django.urls import path
from . import views
# This file defines the URL patterns for the 'website' app in the DCRM project.

urlpatterns = [
    path('', views.home, name='home'),      
    path('login/', views.login_user, name='login'),     
    path('logout/', views.logout_user, name='logout'),     
    path('register/', views.register_user, name='register'),  
] 

