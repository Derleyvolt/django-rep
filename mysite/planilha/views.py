from django.shortcuts                 import render
from rest_framework.viewsets          import ModelViewSet
from rest_framework.decorators        import action
from .models                          import PlanilhaModel
from .serializers.PlanilhaSerializer  import PlanilhaSerializer
from rest_framework.response          import Response

# Create your views here.

# class PlanilhaView(ViewSet):
#     permission_classes = (IsAuthenticated,)
    
#     def listar(self, request):
#         queryset = PlanilhaModel.objects.all()
#         serializer = PlanilhaSerializer(queryset, many=True)
#         return Response(serializer.data)

#     # RATO
#     def atualizar(self, request):
#         for i in request.data:
#             serializer = PlanilhaSerializer(data=i)
#             if not serializer.is_valid():
#                 return Response(serializer.data, status=400)

#         for i in request.data:
#             serializer = PlanilhaSerializer(data=i)
#             if serializer.is_valid():
#                 serializer.save()
        
#         return Response("Sucess", status=200)

#     def retrieve_by_name(self, request, nome):
#         query      = PlanilhaModel.objects.filter(nome_funcionario = nome)
#         serializer = PlanilhaSerializer(query, many=True)
#         return Response(serializer.data, status=200)

#     def retrieve_by_salary(self, request, salary):
#         query      = PlanilhaModel.objects.filter(salario__gte = 5.0)
#         serializer = PlanilhaSerializer(query, many=True)
#         return Response(serializer.data, status=200)

class PlanilhaViewset(ModelViewSet):
    queryset         = PlanilhaModel.objects.all()
    serializer_class = PlanilhaSerializer

    # primary key

    @action(detail=False, methods=['post'], url_path='items')
    def items_not_done(self, request):
        try:
            user_count = PlanilhaModel.objects.get(telefone=request.data['telefone'])
        except:
            return Response("O item nao existe", status=400)

        serializer = self.get_serializer(user_count)

        return Response(serializer.data, status=200)