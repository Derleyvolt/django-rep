from rest_framework import serializers
from ..models import PlanilhaModel

class PlanilhaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PlanilhaModel
        fields = '__all__'