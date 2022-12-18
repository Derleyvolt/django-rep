from django.contrib import admin
from django.urls import path
from .views import PlanilhaView

urlpatterns = [
    path('planilha', PlanilhaView.as_view({'get' : 'listar', 'post' : 'atualizar'})),
    path('planilha/<str:nome>', PlanilhaView.as_view({'get' : 'retrieve_by_name'})),
    path('planilha/<int:salary>', PlanilhaView.as_view({'get' : 'retrieve_by_salary'})),
]
