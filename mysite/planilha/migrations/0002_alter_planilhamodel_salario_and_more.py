# Generated by Django 4.1.2 on 2022-12-07 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planilha', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planilhamodel',
            name='salario',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='planilhamodel',
            name='salario_total',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
