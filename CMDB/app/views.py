from django.shortcuts import render

# Create your views here.

from .models import *
from .utilities.utilities import get_active_ports
import re


def services(request):
    context = { "servizi" : get_active_ports() }
    return render(request, "services.html", context)


def homepage(request):
    agents = AgentDB.objects.prefetch_related("disks").all()    
    return render(request, "index.html", {"agents": agents})


class LogLine():
    def __init__(self, timestamp, percorso, type_request, answer_request):
        self.timestamps = timestamp, 
        self.percorso = percorso
        self.type_request = type_request
        self.answer_request = answer_request


def find_timestamp(line):
    """
    [05/Apr/2025:09:26:59 +0200]
    """
    re_match = re.search(r"(\[.*])", line)
    if re_match:
        return re_match.group(0)


def find_percorso(line):
    """
    percorsi come:
    /
    /dashboard/
    /dashboard/images/fastly-logo.png
    /phpmyadmin/themes/pmahomme/img/s_loggoff.png
    """
    re_match = re.search(r'"(?:\w+)?\s+([a-zA-Z0-9\-_./]+)', line)
    if re_match:
        return re_match.group(1)


def find_type_request(line):
    re_match = re.search(r"(GET)|(POST)|(PUT)|(DELETE)|(HEAD)|(OPTIONS)", line)
    if re_match:
        return re_match.group(0)


def find_answer_request(line):
    re_match = re.search(r"\s\d{3}\s", line)
    if re_match:
        return re_match.group(0).strip()


def access(request):
    context = { 
        "logs" : []
    }

    with open("./flussi/access.log", "r") as f_log:
        for line in f_log:
            
            context["logs"].append(
                LogLine(
                    timestamp = find_timestamp(line),
                    percorso = find_percorso(line),
                    type_request = find_type_request(line),
                    answer_request = find_answer_request(line)
                )
            )

    return render(request, "access.html", context)

