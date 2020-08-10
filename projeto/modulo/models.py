from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User



class Miniteste(models.Model):
    nota = models.IntegerField(default=-1)
    numero = models.IntegerField(default=-1)
    descricao = models.CharField(max_length=200, default="Geral")

class QuestaoMT(models.Model):
    texto_questo = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data de publicacao')
    miniteste = models.ForeignKey(Miniteste, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto_questo

    def foi_publicada_recentemente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)

class RespostaMT(models.Model):
    questao = models.ForeignKey(QuestaoMT, on_delete=models.CASCADE)
    texto_resposta = models.CharField(max_length=200)
    resposta_certa = models.BooleanField(default=False)

class Questao(models.Model):
    questao_texto = models.CharField(max_length=200)
    pub_data =models.DateTimeField('data de publicacao')
    username = models.CharField(max_length=200,default='')

    def foi_publicada_recentemente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.questao_texto

class Denuncia(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    nome_denunciante = models.CharField(max_length=200)
    data = models.DateTimeField('data de denuncia')


class Resposta(models.Model):
    questao = models.ForeignKey(Questao,
    on_delete=models.CASCADE)
    resposta_texto = models.CharField(max_length=200)
    resposta_dono = models.CharField(max_length=200)
    resposta_pub_data = models.DateTimeField('data de publicacao')
    #denuncias = models.IntegerField(default=0)
    path= models.CharField(default='', max_length=200)


    def __str__(self):
        return self.resposta_texto

class Denuncia_Resposta(models.Model):
    resposta = models.ForeignKey(Resposta, on_delete=models.CASCADE)
    nome_denunciante = models.CharField(max_length=200)
    data = models.DateTimeField('data de denuncia')



class Aluno(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE )
    nome_completo = models.CharField(max_length=200, default='')
    nota_trabalho = models.IntegerField(default=-1)
    nota_final = models.IntegerField(default= -1)
    ultima_semana = models.IntegerField(default=0)

    def __str__(self):
        return self.nome_completo

    def calcular_nota_final(self):
        exercicios = self.exercicio_set.all()
        soma = 0
        if len(exercicios)==0:
            return 'Não disponivel'
        else:
            for i in exercicios:
                soma += i.nota
            media = soma / len(exercicios)
            media_exercicio = float(media*20)
            if self.nota_trabalho != -1:
                nota_final = media_exercicio*0.15 + self.nota_trabalho*0.85
                return int(nota_final + 0.5)
            else:
                return 'Não disponível'



class Exercicio(models.Model):
    semana= models.IntegerField(default=-1)
    nota = models.DecimalField(max_digits=2, decimal_places=1)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)

class SlidePasta(models.Model):
    nome_pasta = models.CharField(max_length=200)


class Ficheiro(models.Model):
    nome_ficheiro=models.CharField(max_length=200)
    slidepasta = models.ForeignKey(SlidePasta, on_delete=models.CASCADE)



class ExercicioSlide(models.Model):
    nome_exercicio = models.CharField(max_length=200)


class ExercicioFicheiro(models.Model):
    nome_ficheiro= models.CharField(max_length=200)
    exercicio_Slide = models.ForeignKey(ExercicioSlide, on_delete=models.CASCADE)

class Data_Avaliacao(models.Model):
    data = models.DateTimeField('data de avalição')
    sala = models.CharField(max_length=10)
    descrição = models.CharField(max_length=200)




class Semana(models.Model):
    numero=models.IntegerField()


class Aula(models.Model):
    dia = models.CharField(max_length=200)
    hora_inicio = models.CharField(max_length=100)
    hora_fim = models.TimeField('hora do fim da aula')
    sala = models.CharField(max_length=200, default='')
    semana = models.ForeignKey(Semana, on_delete=models.CASCADE)

class Miniteste_Aluno(models.Model):
    minitestes = models.ForeignKey(Miniteste, on_delete=models.CASCADE)
    id_aluno = models.IntegerField(default=0)
