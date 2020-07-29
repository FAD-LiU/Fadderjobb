# Generated by Django 2.0.9 on 2019-02-05 11:21

from django.db import migrations, models
import fadderanmalan.models


class Migration(migrations.Migration):

    dependencies = [
        ('fadderanmalan', '0002_auto_20181113_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='hidden',
            field=models.BooleanField(default=False, help_text='Om jobbet ska döljas från frontend:en. Har högre prioritet än datumen nedan'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='hidden_after',
            field=models.DateField(default=fadderanmalan.models.default_hidden_after, help_text='Från när jobbet ska döljas.'),
        ),
        migrations.AddField(
            model_name='job',
            name='hidden_until',
            field=models.DateField(default=fadderanmalan.models.default_hidden_until, help_text='Från när jobbet ska visas.'),
        ),
        migrations.AddField(
            model_name='job',
            name='locked_after',
            field=models.DateField(default=fadderanmalan.models.default_locked_after, help_text='Från när jobbet ska vara låst.'),
        ),
        migrations.AddField(
            model_name='job',
            name='locked_until',
            field=models.DateField(default=fadderanmalan.models.default_locked_until, help_text='Från när jobbet ska låsas upp.'),
        ),
        migrations.AlterField(
            model_name='job',
            name='locked',
            field=models.BooleanField(help_text='Om jobbet ska vara låst. Har högre prioritet än datumen nedan.'),
        ),
    ]
