from .models            import Vigile, Auto, Contravvenzione, Log
from django.shortcuts   import render, redirect

from django.core        import serializers # converte tabella in formato json
from django.http        import JsonResponse # lo uso per renderizzare l'API

from datetime           import datetime


def homepage(request):
    if request.method == "POST":

        vigile_id       = request.POST["vigile"]
        targa           = request.POST["targa"]
        luogo           = request.POST["luogo"]
        tipo_infrazione = request.POST["tipo_infrazione"]
        importo         = request.POST["importo"] 

        vigile = Vigile.objects.get(id = vigile_id)
        auto, created = Auto.objects.get_or_create(
            targa           = targa,
            marca           = request.POST["marca"],
            modello         = request.POST["modello"],
            proprietario    = request.POST["proprietario"]
        )

        Contravvenzione.objects.create(
            vigile          = vigile,
            auto            = auto,
            datetime        = datetime.now(),
            luogo           = luogo,
            tipo_infrazione = tipo_infrazione,
            importo         = importo
        )
  
        Log.objects.create(
            descrizione_evento = f"eseguito richiesta di tipo post alla homepage dal vigile: {vigile_id}",
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
    table_to_json = serializers.serialize('json', contravvenzioni)
    return JsonResponse(table_to_json, safe=False)