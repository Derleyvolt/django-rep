# Generated by Django 4.1.3 on 2023-01-05 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorecidosmodel',
            name='cpf',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
