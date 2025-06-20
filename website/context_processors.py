from .models import Cliente, User  # Adjust imports based on your models

def modal_context(request):
    if request.user.is_authenticated:
        return {
            'clientes': Cliente.objects.all(),
            'agentes': User.objects.all
            #'agentes': User.objects.filter(is_staff=True)  # or however you identify agents
        }
    return {}