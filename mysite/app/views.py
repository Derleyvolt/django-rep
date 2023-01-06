from django.shortcuts            import render
from rest_framework.viewsets     import ModelViewSet
from rest_framework.viewsets     import ViewSet
from rest_framework.views        import APIView
from .models                     import ProjetoModel, FavorecidosModel
from .serializers.serializer     import ProjetoSerializer, FavorecidoSerializer
from rest_framework.response     import Response
from rest_framework.decorators   import action
from rest_framework.permissions  import IsAuthenticated

# Create your views here.

class ProjetoView(ViewSet):
    # permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path='criar_favorecido')
    def criar_favorecido(self, request):
        serializer = FavorecidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Success", status=200)
        return Response("Failure", status=400)
    
    @action(methods=['GET'], detail=False, url_path='obter_tudo_favorecido')
    def obter_tudo_favorecido(self, request):
        queryset   = FavorecidosModel.objects.all()
        serializer = FavorecidoSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    @action(methods=['GET'], detail=True, url_path='obter_favorecido')
    def obter_favorecido(self, request, pk=None):
        try:
            instance   = FavorecidosModel.objets.get(id=pk)
        except:
            return Response("Failure", status=400)
        
        serializer = FavorecidoSerializer(instance)
        return Response(serializer.data, status=200)

    @action(methods=['POST'], detail=False, url_path='criar_projeto')
    def criar(self, request):
        serializer = ProjetoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Success", status=200)
        return Response("Failure", status=400)

    @action(methods=['GET'], detail=True, url_path='obter_projeto')
    def obter(self, request, pk=None):
        try:
            instance = ProjetoModel.objects.get(id=pk)
        except:
            return Response("Failure", status=400)

        serializer = ProjetoSerializer(data=instance)
        return Response(serializer.data, status=200)

    @action(methods=['GET'], detail=False, url_path='obter_tudo')
    def obter_tudo(self, request):
        result      = []
        queryset    = ProjetoModel.objects.all()
        serializer  = ProjetoSerializer(queryset, many=True)

        for u in serializer.data:
            try:
                dados_favorecidos = FavorecidosModel.objects.get(id=u['id_coordenador'])
                u['nome_coordenador'] = dados_favorecidos.nome
                u['cpf_coordenador']  = dados_favorecidos.cpf
                u['cnpj_coordenador'] = dados_favorecidos.cnpj

                dados_favorecidos = FavorecidosModel.objects.get(id=u['id_proponente'])

                u['nome_proponente']  = dados_favorecidos.nome
                u['cpf_proponente']   = dados_favorecidos.cpf
                u['cnpj_proponente']  = dados_favorecidos.cnpj

                result.append(u)
                result[-1].pop('id_coordenador')
                result[-1].pop('id_proponente')
            except:
                return Response("O id do coordenador ou proponente nao foi/foram encontrado(s)", status=400)

        return Response(result, status=200)

    @action(methods=['GET'], detail=False, url_path='obter_tudo_minimal')
    def obter_tudo_minimal(self, request):
        result      = []
        queryset    = ProjetoModel.objects.all()
        serializer  = ProjetoSerializer(queryset, many=True)

        for u in serializer.data:
            result.append({ "id" : u['id'], "titulo": u['titulo'] })

        return Response(result, status=200)