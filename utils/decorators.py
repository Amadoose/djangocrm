from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def auth_required(view_func=None, login_url=None):
    """Reusable authentication decorator"""
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url or '/login/'
    )
    return actual_decorator(view_func) if view_func else actual_decorator