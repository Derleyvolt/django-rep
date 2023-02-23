from django.db import models
#from ..account.models import CustomUser
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation   import gettext as _
from .managerUser import UserManager
# Create your models here.

class UserEmailValidator(models.Model):
    id    = models.CharField(primary_key=True, unique=True, max_length=150)
    email = models.CharField(max_length=150)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )

    is_active  = models.BooleanField(default=True)   
    staff      = models.BooleanField(default=False) # a admin user; non super-user
    admin      = models.BooleanField(default=False) # a superuser
    username   = models.CharField(max_length=150, blank=True, null=True)

    objects = UserManager()

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Username & Password are required by default.

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

class FavorecidosModel(models.Model):
    nome   = models.CharField(max_length=150)
    cpf    = models.CharField(max_length=150, blank=True, null=True, unique=True)
    cnpj   = models.CharField(max_length=150, blank=True, null=True)

class ProjetoModel(models.Model):
    titulo            = models.CharField(max_length=150)
    contrato          = models.CharField(max_length=150)
    num_sap           = models.IntegerField()
    id_coordenador    = models.ForeignKey(FavorecidosModel, on_delete=models.CASCADE, related_name='id_coordenador', db_column='id_coordenador')
    id_proponente     = models.ForeignKey(FavorecidosModel, on_delete=models.CASCADE, related_name='id_proponente',  db_column='id_proponente')
    id_usuario        = models.ForeignKey(CustomUser,       on_delete=models.CASCADE, related_name='id_usuario',     db_column='id_user')
    data_inicial      = models.DateField()
    data_final        = models.DateField()


class RubricaModel(models.Model):
    id         = models.CharField(primary_key=True, max_length=100, unique=True)
    descricao  = models.CharField(max_length=200, unique=True)

class TipoMovimentacaoModel(models.Model):
    descricao = models.CharField(primary_key=True, max_length=150, unique=True)

# RELAÇÃO 1:N COM TagModel  [EDITADO]
class ExtratoModel(models.Model):
    id_projeto            = models.ForeignKey(ProjetoModel, on_delete=models.CASCADE, related_name='id_projeto', db_column='id_projeto')
    id_movimentacao       = models.ForeignKey(TipoMovimentacaoModel, on_delete=models.CASCADE, related_name='id_movimentacao', db_column='id_movimentacao')
    data                  = models.DateField()
    id_rubrica            = models.ForeignKey(RubricaModel, on_delete=models.CASCADE, related_name='id_rubrica', db_column='id_rubrica')
    id_favorecido         = models.ForeignKey(FavorecidosModel, on_delete=models.CASCADE, related_name = 'id_favorecido', db_column='id_favorecido')
    valor                 = models.FloatField()
    #id_tag                = models.ForeignKey(TagModel, on_delete=models.CASCADE, related_name = 'id_tag', db_column='id_tag')
    observacao            = models.CharField(max_length=150, blank=True)
    data_documento        = models.DateField()
    data_pagamento        = models.DateField()
    #

class TagModel(models.Model):
    descricao   = models.CharField(max_length=150, unique=True, primary_key=True)

class TagExtratoModel(models.Model):
    id_extrato  = models.ForeignKey(ExtratoModel, on_delete=models.CASCADE, related_name = 'id_extrato', db_column='id_extrato')
    id_tag      = models.ForeignKey(TagModel, on_delete=models.CASCADE, related_name = 'id_tag', db_column='id_tag', blank=True, null=True)