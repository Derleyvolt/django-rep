# Generated by Django 4.1.2 on 2022-12-23 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_rename_login_customusermodel_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customusermodel',
            old_name='username',
            new_name='login',
        ),
    ]
