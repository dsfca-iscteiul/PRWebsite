# Generated by Django 2.1.7 on 2019-05-02 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modulo', '0004_auto_20190430_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Denuncia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_denunciante', models.CharField(max_length=200)),
                ('data', models.DateTimeField(verbose_name='data de denuncia')),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo.Questao')),
            ],
        ),
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_pasta', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=1000)),
            ],
        ),
    ]
