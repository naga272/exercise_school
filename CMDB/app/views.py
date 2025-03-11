from django.shortcuts import render

# Create your views here.

from .models import *
from .utilities.utilities import get_active_ports


def services(request):
    context = { "servizi" : get_active_ports() }
    return render(request, "services.html", context)


def homepage(request):
    agents = AgentDB.objects.prefetch_related("disks").all()    
    return render(request, "index.html", {"agents": agents})
