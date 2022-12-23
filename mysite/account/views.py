from rest_framework.viewsets          import ViewSet
from rest_framework.response          import Response
from .models                          import CustomUserModel
from .serializers.serializer          import AccountSerializer

# Create your views here.

class UserAccountView(ViewSet):

    def cadastrar(self, request):
        user = AccountSerializer(data=request.data)

        if user.is_valid():
            user.save()
            return Response(user.data, status=200)
        
        return Response(status=400)

    def connect(self, request):
        query = CustomUserModel.objects.filter(username = request.data['username'])

        if query:
            return Response(status=200)
        return Response(status=400)

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

