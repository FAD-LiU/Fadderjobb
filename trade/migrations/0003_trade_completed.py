# Generated by Django 2.1.7 on 2019-04-16 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20190414_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]