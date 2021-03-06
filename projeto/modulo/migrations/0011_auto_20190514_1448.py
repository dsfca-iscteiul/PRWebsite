# Generated by Django 2.1.7 on 2019-05-14 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modulo', '0010_auto_20190514_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(max_length=200)),
                ('hora_inicio', models.CharField(max_length=100)),
                ('hora_fim', models.TimeField(verbose_name='hora do fim da aula')),
                ('sala', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Semana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='aula',
            name='semana',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo.Semana'),
        ),
    ]
