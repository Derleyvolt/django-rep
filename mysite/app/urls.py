from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProjetoView, UserAccountView, RubricaView, TagView, TipoMovimentacaoView, ExtratoView
from rest_framework_simplejwt import views as jwt_views

router = SimpleRouter()

router.register('', ProjetoView,            basename='projetoview')
router.register('', RubricaView,            basename='rubricaview')
router.register('', TagView,                basename='tagview')
router.register('', TipoMovimentacaoView,   basename='tipomovimentacaoview')
router.register('', ExtratoView,            basename='extratoview')

urlpatterns = [
    path('cadastrar/',      include(router.urls)),

    path('cadastrar_usuario/',      UserAccountView.as_view({'post' : 'cadastrar'})),
    path('obter_id_usuario/',       UserAccountView.as_view({'get'  : 'obter_id'})),
    path('token/',          jwt_views.TokenObtainPairView.as_view(),  name ='token_obtain_pair'),
    path('token/refresh/',  jwt_views.TokenRefreshView.as_view(),     name ='token_refresh'),
]