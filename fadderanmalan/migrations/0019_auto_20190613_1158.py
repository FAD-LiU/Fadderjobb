# Generated by Django 2.0.9 on 2019-06-13 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fadderanmalan', '0018_remove_equipmentownership_returned'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='date',
            new_name='start_date',
        ),
    ]