from django.db import models

# Create your models here.

"""
    La classe Meta la uso per evitare che le tabelle vengano create con un nome sbagliato.
    da vigile (senza classe Meta) diventerebbe vigiles (plurale in inglese, e' l'unica cosa che disprezzo di django)
"""

class Vigile(models.Model):
    matricola = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} {self.cognome}"

    class Meta:
        verbose_name = "Vigile"
        verbose_name_plural = "Vigili"


class Auto(models.Model):
    targa = models.CharField(max_length=10, unique=True)
    colore = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.targa} - {self.colore}"

    class Meta:
        verbose_name = "Auto"
        verbose_name_plural = "Auto"


class Guidatore(models.Model):
    cod_fisc = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} - {self.cognome} - {self.cod_fisc}"

    class Meta:
        verbose_name = "Guidatore"
        verbose_name_plural = "Guidatori"


class Contravvenzione(models.Model):
    vigile = models.ForeignKey(Vigile, on_delete=models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    guidatore = models.ForeignKey(Guidatore, on_delete=models.CASCADE)

    luogo = models.CharField(max_length=200)
    datetime = models.CharField(max_length=200)
    tipo_infrazione = models.CharField(max_length=100)
    importo = models.DecimalField(max_digits=10, decimal_places=2, default=200.00)

    def __str__(self):
        return f"Contravvenzione {self.id} - {self.auto.targa}"

    class Meta:
        verbose_name = "Contravvenzione"
        verbose_name_plural = "Contravvenzioni"


class Log(models.Model):
    descrizione_evento  = models.CharField(max_length = 200)
    datetime            = models.CharField(max_length = 200)

