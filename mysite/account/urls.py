from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 
from .views import UserAccountView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('cadastrar/',      UserAccountView.as_view({'post' : 'cadastrar'})),
    path('obter_id/',       UserAccountView.as_view({'get'  : 'obter_id'})),
    path('token/',         jwt_views.TokenObtainPairView.as_view(),  name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),     name ='token_refresh'),
]