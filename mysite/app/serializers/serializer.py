from rest_framework import serializers
from ..models import ProjetoModel, FavorecidosModel

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ProjetoModel
        fields  = '__all__'

class FavorecidoSerializer(serializers.ModelSerializer):
    class Meta:
        model   = FavorecidosModel
        fields  = '__all__'