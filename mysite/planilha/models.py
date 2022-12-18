from django.db import models

# Create your models here.

class PlanilhaModel(models.Model):
    nome_funcionario             = models.CharField(max_length=100)
    salario                      = models.DecimalField(decimal_places=2, max_digits=5)
    telefone                     = models.CharField(max_length=100)
    quantidade_dias_trabalhados  = models.IntegerField()
    salario_total                = models.DecimalField(decimal_places=2, max_digits=5)