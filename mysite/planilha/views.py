from django.shortcuts                 import render
from rest_framework.viewsets          import ViewSet
from .models                          import PlanilhaModel
from .serializers.PlanilhaSerializer  import PlanilhaSerializer
from rest_framework.response          import Response
from rest_framework.permissions       import IsAuthenticated

# Create your views here.

class PlanilhaView(ViewSet):
    permission_classes = (IsAuthenticated,)
    
    def listar(self, request):
        queryset = PlanilhaModel.objects.all()
        serializer = PlanilhaSerializer(queryset, many=True)
        return Response(serializer.data)

    # RATO
    def atualizar(self, request):
        for i in request.data:
            serializer = PlanilhaSerializer(data=i)
            if not serializer.is_valid():
                return Response(serializer.data, status=400)

        for i in request.data:
            serializer = PlanilhaSerializer(data=i)
            if serializer.is_valid():
                serializer.save()
        
        return Response("Sucess", status=200)

    def retrieve_by_name(self, request, nome):
        query      = PlanilhaModel.objects.filter(nome_funcionario = nome)
        serializer = PlanilhaSerializer(query, many=True)
        return Response(serializer.data, status=200)

    def retrieve_by_salary(self, request, salary):
        query      = PlanilhaModel.objects.filter(salario__gte = 5.0)
        serializer = PlanilhaSerializer(query, many=True)
        return Response(serializer.data, status=200)