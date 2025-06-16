from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.simple_tag
def toggle_sort(request, field):
    dict_ = request.GET.copy()
    current = dict_.get('sort', '')
    
    if current.startswith('-') and current.lstrip('-') == field:
        new_sort = field  # Remove descending if already descending
    elif current == field:
        new_sort = f'-{field}'  # Add descending if ascending
    else:
        new_sort = field  # Default to ascending
    
    dict_['sort'] = new_sort
    return dict_.urlencode()