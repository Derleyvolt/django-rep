from rest_framework.viewsets          import ViewSet
from rest_framework.viewsets          import ModelViewSet
from rest_framework.response          import Response
from .models                          import CustomUser
from .serializers.serializer          import UserSerializer
from rest_framework_simplejwt.tokens  import RefreshToken
from django.contrib.auth.hashers      import make_password
from django.contrib.auth.hashers      import check_password

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
