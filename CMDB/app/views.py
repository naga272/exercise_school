from django.shortcuts import render

# Create your views here.

from .models import *


def homepage(request):
    agents = AgentDB.objects.prefetch_related("disks").all()    
    return render(request, "index.html", {"agents": agents})
