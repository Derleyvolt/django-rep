from django.contrib import admin
from .models import ProjetoModel, FavorecidosModel

# Register your models here.

admin.site.register(ProjetoModel)
admin.site.register(FavorecidosModel)