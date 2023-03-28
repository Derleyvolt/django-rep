from collections import OrderedDict
from django.shortcuts             import render
from rest_framework.viewsets      import ModelViewSet
from rest_framework.viewsets      import ViewSet
from rest_framework.views         import APIView
from .models                      import ProjetoModel, FavorecidosModel, CustomUser, TagModel, RubricaModel, TipoMovimentacaoModel, ExtratoModel, TagExtratoModel, UserEmailValidator, ExecutorModel
from .serializers.serializer      import ProjetoSerializer, FavorecidoSerializer, UserSerializer, TagSerializer, RubricaSerializer, TipoMovimentacaoSerializer, ExtratoSerializer, TagExtratoSerializer, UserEmailValidatorSerializer, ExecutorSerializer
                                         
from rest_framework.response      import Response
from rest_framework.decorators    import action
from rest_framework.permissions   import IsAuthenticated
from django.contrib.auth.hashers  import check_password
from django.core.mail             import send_mail
import random

# Create your views here.

def genRandomCode():
    code = ''
    for i in range(10):
        code += str(random.randint(0, 9))
    return code

class UserAccountView(ViewSet):
    def validar_email(self, request):
        try:
            userFilter = CustomUser.objects.filter(email=request.data['email'])

            if userFilter:
                return Response('Email já cadastrado', status=400)

            while True:
                code = genRandomCode()
                if not UserEmailValidator.objects.filter(id=code):
                    break

            send_mail(
                'Codigo de confirmação',
                'Seu código de confirmação é ' + code,
                'missvegastop@gmail.com',
                [request.data['email']],
                fail_silently=False,
            )
        
            obj = UserEmailValidator.objects.create(id=code, email=request.data['email'])
            obj.save()

            return Response(status=200)
        except:
            return Response('Algum erro ocorreu', status=400)

    def cadastrar(self, request):
        try:
            user = UserSerializer(data=request.data)
            code = request.data['codigo']

            if not UserEmailValidator.objects.filter(id=code):
                return Response('Código inválido', status=400)

            if user.is_valid():
                UserEmailValidator.objects.filter(email=request.data['email']).delete()
                CustomUser.objects.create_user(request.data['email'], request.data['password'], request.data['documento'], request.data['username'])
                return Response(user.data, status=200)
            return Response(status=400)

        except:
            return Response(status=410)

    def obter_id(self, request):
        email    = request.data['email']
        password = request.data['password']

        try:
            query = CustomUser.objects.get(email = email)
        except:
            return Response("Algum erro ocorreu", status=400)

        if check_password(password, query.password):
            return Response({'id' : query.id}, status=200)
        return Response("Algum erro ocorreu", status=400)

class ProjetoView(ViewSet):
    #permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path='criar_projeto')
    def criar(self, request):
        print(request.data)
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

class ExecutorView(ViewSet):
    @action(methods=['POST'], detail=False, url_path='cadastrar_executor')
    def criar_executor(self, request):
        try:
            serializer = ExecutorSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
        except:
            return Response(status=400)
        
    @action(methods=['GET'], detail=False, url_path='listar_executor') 
    def listar_executor(self, request):
        try:
            queryset   = ExecutorModel.objects.all()
            serializer = ExecutorSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response("Error", status=400)

class ExtratoView(ViewSet):
    #permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path='criar_extrato')
    def criar(self, request):
        try:
            tags = request.data['tags']

            serializer = ExtratoSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()

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