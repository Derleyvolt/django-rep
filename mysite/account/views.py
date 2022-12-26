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

    def teste(self, request):
        class UserCustom:
            id = 1
            username = "derley"

        user = UserCustom

        refresh = RefreshToken.for_user(user)

        print({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        })

        return Response(status=200)

        # return {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        # }

    def cadastrar(self, request):
        user = UserSerializer(data=request.data)

        if user.is_valid():
            CustomUser.objects.create_user(request.data['username'], request.data['password'])
            return Response(user.data, status=200)
        
        return Response(status=410)

    def connect(self, request):
        username = request.data['username']
        password = request.data['password']

        query = CustomUser.objects.get(username = username)

        print(query.password)

        if query:
            if check_password(password, query.password):
                return Response({'sucess' : True}, status=200)
        return Response({'sucess' : False}, status=400)

# class UserAccountView(ViewSet):
#     def cadastrar(self, request):
#         password = request.data['password']
#         email    = request.data['email']

#         CustomUser.objects.create_user(email=email, password=password)
        
#         return Response(status=200)

        # if user:
        #     user.password = make_password(password)
        #     user.save(using=self._db)


        # for i in request.data:
        #     serializer = PlanilhaSerializer(data=i)
        #     if not serializer.is_valid():
        #         return Response(serializer.data, status=400)

        # for i in request.data:
        #     serializer = PlanilhaSerializer(data=i)
        #     if serializer.is_valid():
        #         serializer.save()

