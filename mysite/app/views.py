from collections import OrderedDict
from django.shortcuts             import render
from rest_framework.viewsets      import ModelViewSet
from rest_framework.viewsets      import ViewSet
from rest_framework.views         import APIView
from .models                      import ProjetoModel, FavorecidosModel, CustomUser, TagModel, RubricaModel, TipoMovimentacaoModel, ExtratoModel, TagExtratoModel
from .serializers.serializer      import ProjetoSerializer, FavorecidoSerializer, UserSerializer, TagSerializer, RubricaSerializer, TipoMovimentacaoSerializer, ExtratoSerializer, TagExtratoSerializer
                                         
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
    #permission_classes = [IsAuthenticated]

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

class FavorecidoView(ViewSet):
    #permission_classes = [IsAuthenticated]

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
            instance   = FavorecidosModel.objects.get(id=pk)
        except:
            return Response("Failure", status=400)
        
        serializer = FavorecidoSerializer(instance)
        return Response(serializer.data, status=200)

class RubricaView(ViewSet):
    #permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]

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
    #permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path='criar_movimentacao')
    def criar(self, request):
        print(request.data)
        serializer = TipoMovimentacaoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=400)

    # @action(methods=['GET'], detail=True, url_path='obter_movimentacao')
    # def obter_movimentacao(self, request, pk=None):
    #     try:
    #         instance   = TipoMovimentacaoModel.objects.get(descricao=pk)
    #     except:
    #         return Response("Failure", status=400)
        
    #     serializer = TipoMovimentacaoSerializer(instance)
    #     return Response(serializer.data, status=200)

    @action(methods=['GET'], detail=False, url_path='listar_movimentacao')
    def listar(self, request):
        queryset   = TipoMovimentacaoModel.objects.all()
        serializer = TipoMovimentacaoSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

# class TagExtratoView(ViewSet):
#     @action(methods=['GET'], detail=false, url_path='obter_extratos')
#     def obter_extratos(self, request, pk=None):
#         try:
#             queryset = ExtratoModel.objects.filter(id_projeto=pk)
#         except ExtratoModel.DoesNotExist:
#             return Response(status=200)
        
#         serializer = ExtratoSerializer(queryset, many=True)
#         return Response(serializer.data, status=200)  

class ExtratoView(ViewSet):
    #permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path='criar_extrato')
    def criar(self, request):
        try:
            tags = request.data['tags']

            serializer = ExtratoSerializer(data=request.data)
            
            print(tags)

            if serializer.is_valid():
                serializer.save()


                # if len(tags) > 0:
                #     serializerTagExtrato = TagExtratoSerializer(data=)

                for e in tags:
                    dataTagExtrato = { "id_extrato": serializer.data['id'], "id_tag": e }
                    serializerTagExtrato  = TagExtratoSerializer(data=dataTagExtrato)
                    if serializerTagExtrato.is_valid():
                        serializerTagExtrato.save()
                
                return Response(serializer.data, status=201)
            return Response(status=400)
        except:
            return Response(status=400)

    @action(methods=['GET'], detail=True, url_path='obter_extratos')
    def obter_extratos(self, request, pk=None):
        try:
            queryset          = ExtratoModel.objects.filter(id_projeto=pk)
            serializedExtrato = ExtratoSerializer(queryset, many=True)

            for ex in serializedExtrato.data:
                idExtrato = ex.get('id')
                try:
                    tagQuerySet   = TagExtratoModel.objects.filter(id_extrato=idExtrato)
                    serializedTagExtrato = TagExtratoSerializer(tagQuerySet, many=True)

                    # coluna id_extrato e id não é útil aqui, é redundante.
                    for ex2 in serializedTagExtrato.data:
                        ex2.pop('id_extrato')
                        ex2.pop('id')

                    ex['tags'] = list(map(lambda e: e['id_tag'],serializedTagExtrato.data))
                except:
                    pass

        except ExtratoModel.DoesNotExist:
            return Response(status=200)
        
        return Response(serializedExtrato.data, status=200)

    @action(methods=['PUT'], detail=True, url_path='update_extrato')
    def update_extrato(self, request, pk=None):
        try:
            obj = ExtratoModel.objects.get(pk=pk)
            obj.__dict__.update(request.data)

            # ForeignKeys
            obj.id_favorecido_id            = request.data['id_favorecido']
            obj.id_rubrica_id               = request.data['id_rubrica']
            obj.id_movimentacao_id          = request.data['id_movimentacao']
            obj.id_projeto_id               = request.data['id_projeto']

            queryset = TagExtratoModel.objects.filter(id_extrato=pk)
            
            tags = request.data['tags']

            # só atualizo as tags necessárias
            for data in queryset:
                if data.id_tag.descricao not in tags:
                    data.delete()
                else:
                    tags.remove(data.id_tag.descricao)
            
            for e in tags:
                dataTagExtrato        = { "id_extrato": pk, "id_tag": e }
                serializerTagExtrato  = TagExtratoSerializer(data=dataTagExtrato)
                if serializerTagExtrato.is_valid():
                    serializerTagExtrato.save()

            obj.save()
            
        except ExtratoModel.DoesNotExist:
            return Response(status=200)

        serializer = ExtratoSerializer(obj)
        return Response(serializer.data, status=200)