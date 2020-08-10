# Generated by Django 2.1.7 on 2019-05-16 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modulo', '0013_miniteste_aluno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visualizacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_aluno', models.IntegerField()),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo.Questao')),
            ],
        ),
    ]