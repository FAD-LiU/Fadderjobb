# Generated by Django 2.1.7 on 2019-04-14 18:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fadderanmalan', '0015_auto_20190414_0856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('requested', models.ManyToManyField(related_name='requested_in_trades', to='fadderanmalan.JobUser')),
                ('sent', models.ManyToManyField(related_name='sent_in_trades', to='fadderanmalan.JobUser')),
            ],
        ),
    ]
