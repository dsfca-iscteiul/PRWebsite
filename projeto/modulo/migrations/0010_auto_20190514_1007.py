# Generated by Django 2.1.7 on 2019-05-14 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo', '0009_data_avaliacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='miniteste',
            name='descricao',
            field=models.CharField(default='Geral', max_length=200),
        ),
        migrations.AddField(
            model_name='miniteste',
            name='numero',
            field=models.IntegerField(default=-1),
        ),
    ]