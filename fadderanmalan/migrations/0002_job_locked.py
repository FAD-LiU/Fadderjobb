# Generated by Django 2.0.9 on 2018-10-11 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fadderanmalan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='locked',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]