from django.db import models

# Create your models here.

class FavorecidosModel(models.Model):
    nome   = models.CharField(max_length=150)
    cpf    = models.CharField(max_length=150, blank=True, null=True, unique=True)
    cnpj   = models.CharField(max_length=150, blank=True, null=True)

class ProjetoModel(models.Model):
    titulo            = models.CharField(max_length=150)
    contrato          = models.CharField(max_length=150)
    num_sap           = models.IntegerField()
    id_coordenador    = models.ForeignKey(FavorecidosModel, on_delete=models.CASCADE, related_name = 'id_coordenador', db_column='id_coordenador')
    id_proponente     = models.ForeignKey(FavorecidosModel, on_delete=models.CASCADE, related_name = 'id_proponente',  db_column='id_proponente')