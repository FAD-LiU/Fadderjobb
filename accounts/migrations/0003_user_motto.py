# Generated by Django 2.0.9 on 2018-11-13 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181113_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='motto',
            field=models.TextField(default='', max_length=100),
            preserve_default=False,
        ),
    ]