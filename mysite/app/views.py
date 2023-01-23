from django.shortcuts             import render
from rest_framework.viewsets      import ModelViewSet
from rest_framework.viewsets      import ViewSet
from rest_framework.views         import APIView
from .models                      import ProjetoModel, FavorecidosModel, CustomUser, TagModel, RubricaModel, TipoMovimentacaoModel, ExtratoModel
from .serializers.serializer      import ProjetoSerializer, FavorecidoSerializer, UserSerializer, TagSerializer, RubricaSerializer, TipoMovimentacaoSerializer, ExtratoSerializer
                                         
from rest_framework.response      import Response
from rest_framework.decorators    import action
from rest_framework.permissions   import IsAuthenticated
from django.contrib.auth.hashers  import check_password

# Create your views here.

class UserAccountView(ViewSet):
    def cadastrar(self, request):
        user = UserSerializer(data=request.data)

        if user.is_valid():
            CustomUser.objects.create_user(request.data['username'], request.data['password'])
            return Response(user.data, status=200)
        
        return Response(status=410)

    def obter_id(self, request):
        username = request.data['username']
        password = request.data['password']

        try:
            query = CustomUser.objects.get(username = username)
        except:
            return Response("Failure", status=400)

        if check_password(password, query.password):
            return Response({'id' : query.id}, status=200)
        return Response("Failure", status=400)

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

def increment_rubrica_id(id, levels = 2):
    if id.replace('.', '') == '333':
        return id;

    # 1.1.1 => permite 3^3-3^2 combinações
    id_ls = list(id.replace('.', ''))

    for i in range(2, 0, -1):
        if (ord(id_ls[i])-ord('0')) < levels:
            id_ls[i] = chr(ord(id_ls[i]) + 1)
            break
        else:
            id_ls[i] = '0'
    
    return ".".join(id_ls)

class RubricaView(ViewSet):
    # @action(methods=['POST'], detail=False, url_path='criar_rubrica')
    # def criar(self, request):
    #     try:
    #         queryset = RubricaModel.objects.latest('id')
    #     except RubricaModel.DoesNotExist:
    #         obj = { "id" : "1.0.0", "descricao" : request.data['descricao'] }

    #         serializer = RubricaSerializer(data=obj)

    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(status=201)

    #     new_rubrica_id = increment_rubrica_id(queryset.id)

    #     serializer = RubricaSerializer(data={ "id" : new_rubrica_id, "descricao" : request.data['descricao'] })

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(new_rubrica_id, status=201)

    #     return Response(status=400)

    @action(methods=['POST'], detail=False, url_path='criar_rubrica')
    def criar(self, request):
        try:
            RubricaModel.objects.get(id=request.data['id'])
        except:
            serializer = RubricaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
        return Response(status=400)

    @action(methods=['GET'], detail=True, url_path='verificar_id_rubrica')
    def verificar_id(self, request, pk=None):
        data = '.'.join(str(pk))
        try:
            obj = RubricaModel.objects.get(id=data)
        except:
            return Response({ 'status' : True}, status=200)
        return Response({ 'status' : False}, status=400)

    @action(methods=['GET'], detail=False, url_path='listar_rubrica')
    def listar(self, request):
        queryset   = RubricaModel.objects.all()
        serializer = RubricaSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

class TagView(ViewSet):
    @action(methods=['POST'], detail=False, url_path='criar_tag')
    def criar(self, request):
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=400)

    @action(methods=['GET'], detail=False, url_path='listar_tag')
    def listar(self, request):
        queryset   = TagModel.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

class TipoMovimentacaoView(ViewSet):
    @action(methods=['POST'], detail=False, url_path='criar_movimentacao')
    def criar(self, request):
        serializer = TipoMovimentacaoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=400)

    @action(methods=['GET'], detail=False, url_path='listar_movimentacao')
    def listar(self, request):
        queryset   = TipoMovimentacaoModel.objects.all()
        serializer = TipoMovimentacaoSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

class ExtratoView(ViewSet):
    @action(methods=['POST'], detail=False, url_path='criar_extrato')
    def criar(self, request):
        serializer = ExtratoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(status=400)

    @action(methods=['GET'], detail=True, url_path='obter_extratos')
    def obter_extratos(self, request, pk=None):
        try:
            queryset = ExtratoModel.objects.filter(id_projeto=pk)
        except ExtratoModel.DoesNotExist:
            return Response(status=200)
        
        serializer = ExtratoSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    
    @action(methods=['PUT'], detail=True, url_path='update_extrato')
    def update_extrato(self, request, pk=None):
        try:
            obj = ExtratoModel.objects.get(pk=pk)
            obj.__dict__.update(request.data)
            obj.save()
        except ExtratoModel.DoesNotExist:
            return Response(status=200)

        serializer = ExtratoSerializer(obj)
        return Response(serializer.data, status=200)