from .models import Movement


def get_sidebar_movements(request):
    return{
        'movements' : Movement.objects.all()[:5]
    }

def all_movements(request):
    return{
        'all_movements' : Movement.objects.order_by('created')
    }