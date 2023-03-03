from rest_framework import serializers
from ..models import ProjetoModel, FavorecidosModel, CustomUser, RubricaModel, TagModel, TipoMovimentacaoModel, ExtratoModel, TagExtratoModel, UserEmailValidator

class UserEmailValidatorSerializer(serializers.ModelSerializer):
    class Meta:
        model   = UserEmailValidator
        fields  = '__all__'

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ProjetoModel
        fields  = '__all__'

class FavorecidoSerializer(serializers.ModelSerializer):
    class Meta:
        model   = FavorecidosModel
        fields  = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model   = CustomUser
        fields  = ['email', 'password']

class TipoMovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model   = TipoMovimentacaoModel
        fields  = ['descricao']

class RubricaSerializer(serializers.ModelSerializer):
    class Meta:
        model   = RubricaModel
        fields  = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model   = TagModel
        fields  = '__all__'

class ExtratoSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ExtratoModel
        fields  = '__all__'

class TagExtratoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TagExtratoModel
        fields = '__all__'

# class TagExtratoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model   = TagModelExtrato
#         fields  = '__all__'