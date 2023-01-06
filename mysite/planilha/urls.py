from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token 
from .views import PlanilhaView
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'planilha', PlanilhaViewset)

urlpatterns = [
    #path('', include(router.urls))
    path('planilha', PlanilhaView.as_view({'get' : 'listar', 'post' : 'atualizar'})),
    path('planilha/<str:nome>', PlanilhaView.as_view({'get' : 'retrieve_by_name'})),
    path('planilha/<int:salary>', PlanilhaView.as_view({'get' : 'retrieve_by_salary'})),
]