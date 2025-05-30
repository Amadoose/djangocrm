from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Render the home page of the DCRM website.
    
    This view handles requests to the root URL and returns the home page template.
    """
    return render(request, 'home.html', {})
