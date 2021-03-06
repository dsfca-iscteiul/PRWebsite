# Generated by Django 2.1.7 on 2019-05-02 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modulo', '0006_auto_20190502_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Denuncia_Resposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_denunciante', models.CharField(max_length=200)),
                ('data', models.DateTimeField(verbose_name='data de denuncia')),
                ('resposta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo.Resposta')),
            ],
        ),
    ]
