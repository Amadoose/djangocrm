def page_title(request):
    # Map URL names to titles
    url_titles = {
        'home': 'Home',
        'quote': 'New Quote',
        'clients': '',
        'users': 'Users',
        'reports': 'Reports',
        'administration': 'Administration',
        'new_client': '',
        'update_client': '',
        'client_detail': '',
        # Add more as needed
    }
    url_name = getattr(request.resolver_match, 'url_name', None)
    return {
        'page_title': url_titles.get(url_name)
    }