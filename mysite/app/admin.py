from django.contrib import admin
from .models import ProjetoModel, FavorecidosModel, CustomUser, RubricaModel, ExtratoModel, TagModel

# Register your models here.

admin.site.register(ProjetoModel)
admin.site.register(FavorecidosModel)
admin.site.register(CustomUser)
admin.site.register(RubricaModel)
admin.site.register(ExtratoModel)
admin.site.register(TagModel)
