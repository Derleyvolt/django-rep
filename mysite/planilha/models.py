from django.db import models

# Create your models here.

class PlanilhaModel(models.Model):
    rubrica               = models.CharField(max_length=100)
    X                     = models.CharField(max_length=100)
    I                     = models.CharField(max_length=100)
    R                     = models.CharField(max_length=100)
    data_pg               = models.DateField()
    ch                    = models.CharField(max_length=100)
    data_recibo           = models.DateField()
    recibo                = models.IntegerField()
    comp                  = models.DateField()
    N                     = models.IntegerField()
    pessoal               = models.CharField(max_length=150)
    favorecido_fornecedor = models.CharField(max_length=150)
    documento             = models.CharField(max_length=150)
    credito               = models.DecimalField(max_digits=10, decimal_places=2)
    debito                = models.DecimalField(max_digits=10, decimal_places=2)
    saldo                 = models.DecimalField(max_digits=10, decimal_places=2)