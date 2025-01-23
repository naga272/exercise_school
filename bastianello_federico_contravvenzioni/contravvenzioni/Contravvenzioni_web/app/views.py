from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.core        import serializers # converte tabella in formato json
from django.http        import JsonResponse # lo uso per renderizzare l'API

from .models            import *
from datetime           import datetime


def homepage(request):
    if request.method == "POST":

        matricola       = request.POST["matricola"]
        targa           = request.POST["targa"]
        colore          = request.POST["colore"]
        luogo           = request.POST["luogo"]
        cod_fisc        = request.POST["cod_fisc"]
        tipo_infrazione = request.POST["tipo_infrazione"]
        importo         = request.POST["importo"]
        nome            = request.POST["nome"]
        cognome         = request.POST["cognome"]


        vigile = Vigile.objects.get(matricola = matricola)


        auto, created = Auto.objects.get_or_create(
            targa   = targa,
            colore  = request.POST["colore"],
        )

        guidatore, created = Guidatore.objects.get_or_create(
            cod_fisc    = cod_fisc,
            nome        = nome,
            cognome     = cognome
        )

        Contravvenzione.objects.create(
            vigile          = vigile,
            auto            = auto,
            guidatore       = guidatore,
            datetime        = datetime.now(),
            luogo           = luogo,
            tipo_infrazione = tipo_infrazione,
            importo         = importo
        )
  
        Log.objects.create(
            descrizione_evento = f"eseguito richiesta di tipo post alla homepage dal vigile: {matricola}",
            datetime = str(datetime.now())
        )
        return redirect("home")
    else:
        context = {
            "vigili" : Vigile.objects.all()
        }
        return render(request, "./index.html", context)


def api_contravvenzioni(request):
    contravvenzioni = Contravvenzione.objects.all()
    table_to_json   = serializers.serialize('json', contravvenzioni)
    return JsonResponse(table_to_json, safe = False)


def get_dats_from_shell(request, matricola, targa, colore, cod_fisc, nome, cognome, luogo, data, reason, importo):
    if request.method == "GET":
        if not all([matricola, targa, colore, cod_fisc, luogo, data, reason, importo]):
            return HttpResponse(status = 400)
 
        vigile = Vigile.objects.get(matricola = matricola)

        auto, created = Auto.objects.get_or_create(
            targa   = targa,
            colore  = colore,
        )

        guidatore, created = Guidatore.objects.get_or_create(
            cod_fisc    = cod_fisc,
            nome        = nome,
            cognome     = cognome
        )

        Contravvenzione.objects.create(
            vigile          = vigile,
            auto            = auto,
            guidatore       = guidatore,
            datetime        = data,
            luogo           = luogo,
            tipo_infrazione = reason,
            importo         = float(importo.replace(" ", "").strip()) # tolgo eventuali spazi messi erroneamente dall'utente
        )

        return HttpResponse(status = 200)
    else:
        return HttpResponse(status = 401)
