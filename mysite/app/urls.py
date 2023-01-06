from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProjetoView

router = SimpleRouter()

router.register('', ProjetoView, basename='projetoview')

urlpatterns = [
    #path('cadastrar', ProjetoView.as_view({ 'GET' : 'get_all', 'POST': 'create' })),
    path('cadastrar/', include(router.urls)),

]