# Generated by Django 4.1.3 on 2023-02-06 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extratomodel',
            name='id_tag',
        ),
        migrations.AddField(
            model_name='tagmodel',
            name='id_extrato',
            field=models.ForeignKey(blank=True, db_column='id_extrato', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_extrato', to='app.extratomodel'),
        ),
    ]
