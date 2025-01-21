from django.contrib import admin

# Register your models here.
from .models        import *


admin.site.register(Contravvenzione)
admin.site.register(Guidatore)
admin.site.register(Vigile)
admin.site.register(Auto)
