from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.urls import reverse
from .models import Questao, Resposta, Miniteste,QuestaoMT,RespostaMT,Aluno,Exercicio, SlidePasta,Ficheiro,ExercicioSlide,ExercicioFicheiro,Denuncia,Denuncia_Resposta, Data_Avaliacao, Semana, Aula
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from decimal import InvalidOperation
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

import time

from django.utils.crypto import get_random_string
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import shutil
from django.utils.datastructures import MultiValueDictKeyError


#Login
def login1(request):
    return  render(request,'modulo/login.html')

def esqueci_palavra_passe(request):
    return render(request, 'modulo/esqueci_palavra_passe.html')

def envia_email(request):
    passe = get_random_string(length=8)
    username = request.POST['username']
    try:
        user= User.objects.get(username=username)
    except(KeyError, User.DoesNotExist):
        return render(request, 'modulo/esqueci_palavra_passe.html', {'error_message': "O nome de utilizador não existe!"})
    else:
        user.set_password(passe)
        user.save()
        email= request.POST['email']
        send_mail('Recuperação da palavra passe Site PR', 'A sua nova palavra-passe do site PR é:'+str(passe), settings.EMAIL_HOST_USER,
        [email],fail_silently=False)
        return render(request, 'modulo/login.html')



def loginview(request):
 username = request.POST['username']
 password = request.POST['password']
 user = authenticate(username=username, password=password)
 if user is not None:
    login(request, user)
    print(user)
    return HttpResponseRedirect (reverse('modulo:index'))
 else:
    return render(request, 'modulo/login.html',{'error_message':"Verifique se introduziu corretamente os seus dados de acesso!"})


#Utilizador
@login_required(login_url="/modulo/login/")
def utilizador(request):
    return render(request, 'modulo/utilizador/utilizador.html',{'user':request.user})

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('modulo:login'))

def alterarpalavrapasse(request):
    return render(request, 'modulo/utilizador/alterarpalavrapasse.html')

def darnota(request):
    alunos= Aluno.objects.all()
    return render(request,'modulo/utilizador/darnota.html',{'alunos':alunos})

def darnota_view(request):
    aluno = Aluno.objects.get(id=request.POST['aluno_id'])
    return render(request, 'modulo/utilizador/darnota_view.html',{'aluno':aluno})

def submeter_nota(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)
    nota_tipo=request.POST['tipo']
    nota = request.POST['nota']
    if nota_tipo == 'exercicio':
        if float(nota) > 1.0:
            return render(request,'modulo/utilizador/darnota_view.html',{'aluno':aluno, 'error_message':"Nota do exercicio não pode ser superior a 1.0"})
        else:
            aluno.ultima_semana += 1
            aluno.save()
            try:
                aluno.exercicio_set.create(semana=aluno.ultima_semana,nota=nota)
            except ValueError:
                return render(request, 'modulo/utilizador/darnota_view.html',{'aluno':aluno,'error_message':"Introduza uma nota válida"})
            except ValidationError:
                return render(request, 'modulo/utilizador/darnota_view.html',
                            {'aluno': aluno, 'error_message': "Introduza uma nota válida"})
    else:
        if float(nota) > 20.0:
            return render(request, 'modulo/utilizador/darnota_view.html',
                          {'aluno': aluno, 'error_message': "Nota do exercicio não pode ser superior a 20.0"})
        else:
            aluno.nota_trabalho = nota
            aluno.save()
    return HttpResponseRedirect(reverse('modulo:index'))

def vernota_alunos(request):
    alunos = Aluno.objects.all()
    return render(request,'modulo/utilizador/vernota_alunos.html',{'alunos':alunos})



def vernota(request, aluno_id):
    trabalho_final ='Não disponível'
    aluno =Aluno.objects.get(pk=aluno_id)
    if aluno.nota_trabalho != -1:
        trabalho_final = aluno.nota_trabalho
    return render(request,'modulo/utilizador/vernota.html',{'aluno':aluno,'trabalho_final':trabalho_final})

def alterarpasse(request):
    antiga = request.POST['old']
    nova = request.POST['new']
    user = request.user
    if antiga == nova:
        user.set_password(nova)
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('modulo:index'))
    else:
        return render(request,'modulo/utilizador/alterarpalavrapasse.html',{'error_message':"As palavras passe não correspondiam, tente novamente"})


@login_required(login_url="/modulo")
def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    user = request.user
    context = {'latest_question_list':latest_question_list, 'error_message':"Não há questões",'user':user}
    return render(request,'modulo/index.html',context)



#####     MINITESTES
def adicionarresposta(request, questao_id):
    resposta = request.POST['resposta']
    path=''
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        path=filename
    q = Questao.objects.get(pk=questao_id)
    q.resposta_set.create(resposta_texto=resposta,resposta_dono=request.user.username,resposta_pub_data= timezone.now(), path=path)
    return HttpResponseRedirect(reverse('modulo:detalhepostforum', args=(questao_id,)))

def minitestes(request):
    minitestes = Miniteste.objects.all()
    user = request.user
    return render(request, 'modulo/conteudos/minitestes.html', {'minitestes': minitestes, 'user':user})

def calcularnota(request, cont):
    notafinal=0
    miniteste=Miniteste.objects.get(pk=cont)
    perguntas = miniteste.questaomt_set.all()
    for questao in perguntas:
        try:
            resposta=RespostaMT.objects.get(pk=request.POST['resposta'+str(questao.id)])
        except(KeyError, RespostaMT.DoesNotExist):
            user = request.user
            return render(request,'modulo/conteudos/minitestes/detalheminiteste.html',{'miniteste':miniteste,'error_message':"selecione a todas as questões",'user':user})
        if resposta.resposta_certa:
            notafinal+= 20/len(perguntas)
    miniteste.miniteste_aluno_set.create(id_aluno=request.user.id)
    return render(request,'modulo/conteudos/minitestes/notafinal.html', {'notafinal':notafinal,'miniteste':miniteste})

def criarminiteste(request):
    return render(request, 'modulo/conteudos/minitestes/criarminiteste.html')

def adicionarminiteste(request):
    nr_miniteste = Miniteste.objects.count() + 1
    descricao_miniteste = request.POST['descricaomt']
    miniteste = Miniteste(nota=-1, numero=nr_miniteste, descricao=descricao_miniteste)
    miniteste.save()
    return HttpResponseRedirect(reverse('modulo:detalheminiteste', args=(miniteste.id,)))


def criarpergunta(request, miniteste_id):
    miniteste = Miniteste(pk=miniteste_id)
    return render(request, 'modulo/conteudos/minitestes/criarpergunta.html',{'miniteste':miniteste})

def adicionarpergunta(request, miniteste_id):
    pergunta = request.POST['pergunta']
    miniteste = Miniteste.objects.get(pk=miniteste_id)
    questao = miniteste.questaomt_set.create(texto_questo=pergunta, pub_data=timezone.now())
    for i in range(1, 5):
        if i == int(request.POST['resposta']):
            questao.respostamt_set.create(texto_resposta=request.POST['r' + str(i)], resposta_certa=True)
        else:
            questao.respostamt_set.create(texto_resposta=request.POST['r' + str(i)], resposta_certa=False)
    questao.save()
    return HttpResponseRedirect(reverse('modulo:detalheminiteste', args=(miniteste.id,)))

def detalheminiteste(request,miniteste_id):
    miniteste=Miniteste.objects.get(pk=miniteste_id)
    questoes=miniteste.questaomt_set.all()
    user=request.user
    alunos=miniteste.miniteste_aluno_set.all()
    ids=[]
    for aluno in alunos:
        ids.append(aluno.id_aluno)
    print(ids)
    return render(request,'modulo/conteudos/minitestes/detalheminiteste.html',{'miniteste':miniteste,'user':user,'ids':ids,'questoes':questoes})

def eliminar_miniteste(request):
    minitestes =Miniteste.objects.all()
    return render(request,'modulo/conteudos/minitestes/eliminar_miniteste.html',{'minitestes':minitestes})

def eliminar(request):
    minitestes=Miniteste.objects.all()
    try:
        miniteste=Miniteste.objects.get(pk= request.POST['miniteste'])
    except(KeyError,Miniteste.DoesNotExist):
        return render(request,'modulo/conteudos/minitestes/eliminar_miniteste.html',{'minitestes':minitestes,'error_message':"Selecione um miniteste para eliminar"})
    else:
        miniteste.delete()
        return HttpResponseRedirect(reverse('modulo:minitestes'))

@login_required(login_url="/modulo")
def conteudos(request):
        return render(request, 'modulo/conteudos.html',{})

@login_required(login_url="/modulo")
def docentes(request):
    return render(request, 'modulo/docentes.html', {})

#Datas
@login_required(login_url="/modulo")
def datasdasavaliacoes(request):
    datas = Data_Avaliacao.objects.all()
    return render(request, 'modulo/datasdasavaliacoes.html', {'datas':datas})

def inserir_data(request):
    descricao=request.POST['descricao']
    data = request.POST['data']
    sala = request.POST['sala']
    data = Data_Avaliacao(descrição=descricao, data=data,sala=sala)
    data.save()
    return HttpResponseRedirect(reverse('modulo:datasdasavaliacoes'))

def eliminar_data(request):
    datas = Data_Avaliacao.objects.all()
    return render(request,'modulo/eliminar_data.html',{'datas':datas})

def apagar_data(request):
    try:
        data= Data_Avaliacao.objects.get(pk=request.POST['data'])
    except(KeyError, Data_Avaliacao.DoesNotExist):
        datas=Data_Avaliacao.objects.all()
        return render(request, 'modulo/eliminar_data.html',{'datas':datas,'error_message':"seleciona uma opção"})
    else:
        data.delete()
        return HttpResponseRedirect(reverse('modulo:datasdasavaliacoes'))

#Forum
@login_required(login_url="/modulo")
def forum(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:]
    user = request.user
    context = {'latest_question_list': latest_question_list, 'error_message': "Não há questões", 'user': user}
    return render(request, 'modulo/forum.html', context)

def enviar_pergunta_modulo(request):
    pergunta=request.POST['pergunta']
    questao= Questao(questao_texto=pergunta, pub_data=timezone.now(),username=request.user.username)
    questao.save()
    return HttpResponseRedirect(reverse('modulo:forum'))

def detalhepostforum(request, questao_id):
    questao = Questao.objects.get(pk=questao_id)
    denunciante = questao.denuncia_set.filter(nome_denunciante=request.user.username)
    denunciante_resposta ={}
    for resposta in questao.resposta_set.all():
        denunciante_resposta[resposta.id]=resposta.denuncia_resposta_set.filter(nome_denunciante=request.user.username)
    return render(request, 'modulo/forum/detalhepostforum.html',{'questao':questao,'denunciante':denunciante,'denunciante_resposta':denunciante_resposta})

def apagar_resposta(request, resposta_id):
    resposta = Resposta.objects.get(pk=resposta_id)
    id = resposta.questao_id
    resposta.delete()
    return HttpResponseRedirect(reverse('modulo:detalhepostforum', args=(id,)))

def apagar_questao(request, questao_id):
    questao=Questao.objects.get(pk=questao_id)
    questao.delete()
    return HttpResponseRedirect(reverse('modulo:forum'))

def denunciar_post(request, questao_id):
    questao = Questao.objects.get(pk=questao_id)
    questao.denuncia_set.create(nome_denunciante=request.user.username,data=timezone.now())
    return HttpResponseRedirect(reverse('modulo:detalhepostforum',args=(questao_id,)))

def denunciar_resposta(request, resposta_id):
    resposta=Resposta.objects.get(pk=resposta_id)
    resposta.denuncia_resposta_set.create(nome_denunciante=request.user.nome, data=timezone.now())
    return HttpResponseRedirect(reverse('modulo:detalhepostforum', args=(resposta.questao.id,)))



def slides(request):
    slides = SlidePasta.objects.all()
    return render(request, 'modulo/conteudos/slides.html', {'slides':slides})

#####     EXERCICIOS
@login_required(login_url="/modulo")
def exercicios(request):
    exercicios= ExercicioSlide.objects.all()
    return render(request,'modulo/conteudos/exercicios.html', {'exercicios':exercicios,'user':request.user})


@login_required(login_url="/modulo")
def eliminar_exercicio(request):
    exercicios = ExercicioSlide.objects.all()
    return render(request, 'modulo/conteudos/exercicios/eliminar_exercicio.html',{'exercicios':exercicios})

def apagar_exercicio(request):
    try:
        exercicio = ExercicioSlide.objects.get(pk=request.POST['exercicio'])
    except(KeyError, ExercicioSlide.DoesNotExist):
        exercicios = ExercicioSlide.objects.all()
        return render(request, 'modulo/conteudos/Exercicios/eliminar_exercicio.html',
                      {'exercicios': exercicios, 'error_message': "Selecione um exercicio"})
    else:
        path = 'modulo/static/modulo/exercicios/' + exercicio.nome_exercicio
        shutil.rmtree(path)
        exercicio.delete()
        return HttpResponseRedirect(reverse('modulo:exercicios'))

def novo_exercicio(request):
    nome = request.POST['nome_exercicio']
    exercicio = ExercicioSlide(nome_exercicio=nome)
    exercicio.save()
    path = 'modulo/static/modulo/exercicios/' + exercicio.nome_exercicio
    os.mkdir(path)
    return HttpResponseRedirect(reverse('modulo:exercicios'))

def detalhe_exercicio(request,exercicio_id):
    exercicio = ExercicioSlide.objects.get(pk=exercicio_id)
    path = 'modulo/static/modulo/exercicios/' + exercicio.nome_exercicio
    lista_ficheiros = os.listdir(path)
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        pathficheiro = 'exercicios/' + exercicio.nome_exercicio
        upload = upload_file(myfile, pathficheiro)
        if upload == 0:
            return render(request, 'modulo/conteudos/exercicios/detalhe_exercicio.html',
                          {'exercicio': exercicio, 'lista_ficheiros': lista_ficheiros, 'user': request.user,
                           'error_message': "O ficheiro já existe"})
        exercicio.exercicioficheiro_set.create(nome_ficheiro=myfile.name)
        return HttpResponseRedirect(reverse('modulo:detalhe_exercicio', args=(exercicio.id,)))
    return render(request, 'modulo/conteudos/exercicios/detalhe_exercicio.html',
                  {'exercicio': exercicio, 'lista_ficheiros': lista_ficheiros, 'user': request.user})



@login_required(login_url="/modulo")
def bibliografia(request):
    return render(request, 'modulo/conteudos/bibliografia.html', {})

#SLIDES
@login_required(login_url="/modulo")
def detalhe_slide(request, slide_id):
    slide = SlidePasta.objects.get(pk=slide_id)
    path = 'modulo/static/modulo/slides/' + slide.nome_pasta
    list = os.listdir(path)
    #nome_ficheiros = retorna_ficheiro(slide.ficheiro_set.all())
    #slides = aux(nome_ficheiros, list)
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        pathficheiro = 'slides/' + slide.nome_pasta
        upload = upload_file(myfile, pathficheiro)
        if upload == 0:
            return render(request, 'modulo/conteudos/slides/detalhe_slide.html',
                          {'slide':slide, 'list':list, 'user':request.user, 'error_message': "O ficheiro já existe"})
        slide.ficheiro_set.create(nome_ficheiro=myfile.name)
        return HttpResponseRedirect(reverse('modulo:detalhe_slide', args=(slide.id,)))
    return render(request, 'modulo/conteudos/slides/detalhe_slide.html',{'slide':slide, 'list':list, 'user':request.user})

def upload_file(myfile, pasta):
    fs = FileSystemStorage()
    fs.save(myfile.name, myfile)
    prevName = 'media/' + myfile.name
    newName = 'modulo/static/modulo/'+pasta+'/' + myfile.name
    try:
        os.rename(prevName, newName)
    except FileExistsError:
        return 0
    return 1

def eliminar_ficheiro_exercicio(request, exercicio_id):
    exercicio = ExercicioSlide.objects.get(pk=exercicio_id)
    ficheiros = exercicio.exercicioficheiro_set.all()
    return render(request, 'modulo/conteudos/exercicios/eliminar_ficheiro.html', {'ficheiros': ficheiros, 'exercicio': exercicio})

def apagar_ficheiroexercicio(request, exercicio_id):
    exercicio = ExercicioSlide.objects.get(pk=exercicio_id)
    try:
        ficheiro= ExercicioFicheiro.objects.get(pk=request.POST['ficheiro'])
    except MultiValueDictKeyError:
        ficheiros = exercicio.exercicioficheiro_set.all()
        return render(request,'modulo/conteudos/exercicios/eliminar_ficheiro.html',{'ficheiros':ficheiros,'exercicio':exercicio, 'error_message':"Selecione um ficheiro"})
    else:
        path = 'modulo/static/modulo/exercicios/'+exercicio.nome_exercicio + '/' + ficheiro.nome_ficheiro
        os.remove(path)
        exercicio_id =ficheiro.exercicio_Slide.id
        ficheiro.delete()
        return HttpResponseRedirect(reverse('modulo:detalhe_exercicio', args=(exercicio_id,)))


def retorna_ficheiro(ficheiros):
    nome_ficheiros = []
    for i in range(len(ficheiros)):
        nome_ficheiros.append(ficheiros[i].nome_ficheiro)
    return nome_ficheiros


def aux(nome_ficheiros, list):
    resul = []
    for ficheiro in list:
        if ficheiro in nome_ficheiros:
            resul.append(ficheiro)
    return resul


def novo_slide(request):
    nome =request.POST['nome_slide']
    slide = SlidePasta(nome_pasta=nome)
    path = 'modulo/static/modulo/slides/' + nome
    try:
        os.mkdir(path)
    except FileExistsError:
        slides = SlidePasta.objects.all()
        return render(request, 'modulo/slides.html', {'slides':slides,'error_message':'Já existe uma pasta com esse nome'})
    slide.save()
    return HttpResponseRedirect(reverse('modulo:slides'))




@login_required(login_url="/modulo")
def eliminar_slide(request):
    slides = SlidePasta.objects.all()
    return render(request, 'modulo/conteudos/slides/eliminar_slides.html',{'slides':slides})

def apagar_slide(request):
    try:
        slide = SlidePasta.objects.get(pk=request.POST['slide'])
    except(KeyError, SlidePasta.DoesNotExist):
        slides = SlidePasta.objects.all()
        return render(request,'modulo/conteudos/slides/eliminar_slides.html',{'slides':slides, 'error_message':"Selecione um slide"})
    else:
        #for i in slide.ficheiro_set.all():
        path = 'modulo/static/modulo/slides/' + slide.nome_pasta
        shutil.rmtree(path)
        slide.delete()
        return HttpResponseRedirect(reverse('modulo:slides'))


@login_required(login_url="/modulo")
def eliminar_ficheiro(request, slide_id):
    slide = SlidePasta.objects.get(pk=slide_id)
    ficheiros = slide.ficheiro_set.all()
    return render(request, 'modulo/conteudos/slides/eliminar_ficheiro.html',{'ficheiros':ficheiros,'slide':slide})


def apagar_ficheiro(request, slide_id):
    slide = SlidePasta.objects.get(pk=slide_id)
    try:
        ficheiro= Ficheiro.objects.get(pk=request.POST['ficheiro'])
    except MultiValueDictKeyError:
        ficheiros = slide.ficheiro_set.all()
        return render(request,'modulo/conteudos/slides/eliminar_ficheiro.html',{'ficheiros':ficheiros,'slide':slide, 'error_message':"Selecione um ficheiro"})
    else:
        path = 'modulo/static/modulo/slides/' + slide.nome_pasta + '/' +ficheiro.nome_ficheiro
        os.remove(path)
        slide_id =ficheiro.slidepasta.id
        ficheiro.delete()
        return HttpResponseRedirect(reverse('modulo:detalhe_slide', args=(slide_id,)))

def lista_negra(request):
    lista_denuncias_questoes=[]
    for questao in Questao.objects.all():
        if questao.denuncia_set.count()>=10:
            lista_denuncias_questoes.append(questao)
    #lista_denuncias_respostas = Resposta.objects.all().filter(denuncias__gt=10)
    return render(request, 'modulo/utilizador/listanegra.html', {'lista_denuncias_questoes':lista_denuncias_questoes})

def eliminar_listanegra(request, resposta_id, nr):
    if int(nr) == 1:
        resposta = Resposta.objects.get(pk=resposta_id)
        resposta.delete()
    else:
        questao= Questao.objects.get(pk=resposta_id)
        questao.delete()
    return HttpResponseRedirect(reverse('modulo:lista_negra'))


def apagarFicheiro(request, pasta_id):
    pasta = Pasta.objects.get(pk=pasta_id)
    try:
        ficheiro = Ficheiro.objects.get(pk=request.POST['ficheiro'])
    except MultiValueDictKeyError:
        ficheiros = pasta.ficheiro_set.all()
        return render(request,'modulo/conteudos/slides/eliminar_ficheiro.html',{'ficheiros':ficheiros,'pasta':pasta, 'error_message':"Selecione um ficheiro"})
    else:
        path = pasta.path + '/' +ficheiro.nome_ficheiro
        os.remove(path)
        pasta_id =ficheiro.pasta.id
        ficheiro.delete()
        return HttpResponseRedirect(reverse('modulo:detalhe_slide', args=(slide_id,)))


@login_required(login_url="/modulo")
def horario(request, semana_id):
    try:
        semana= Semana.objects.get(pk=semana_id)
    except (KeyError, Semana.DoesNotExist):
        semana= Semana.objects.first()
        if semana is None:
            return render(request,'modulo/horario.html', {})
    else:
        semanas = Semana.objects.all()#values_list('id').order_by('id')
        print(semanas)
        aulas_segunda= semana.aula_set.filter(dia='Segunda-Feira')
        aulas_terca = semana.aula_set.filter(dia='Terca-Feira')
        aulas_quarta = semana.aula_set.filter(dia='Quarta-Feira')
        aulas_quinta = semana.aula_set.filter(dia='Quinta-Feira')
        aulas_sexta = semana.aula_set.filter(dia='Sexta-Feira')
        print(aulas_terca)
        return render(request,'modulo/horario.html', {'aulas_segunda':aulas_segunda, 'aulas_terca':aulas_terca,
                                                        'aulas_quarta':aulas_quarta, 'aulas_quinta':aulas_quinta,
                                                        'aulas_sexta':aulas_sexta, 'semanas':semanas, 'user':request.user})


def inserir_aula(request):
    semanas = Semana.objects.all()
    return render(request,'modulo/horario/inserir_aula.html',{'semanas':semanas})

def detalhe_semana(request, semana_id):
    semana= Semana.objects.get(pk=semana_id)
    aulas = semana.aula_set.all()
    return render(request,'modulo/horario/detalhe_semana.html', {'semana':semana,'aulas':aulas})

def criar_semana(request):
    semana = Semana(numero=1)
    semana.save()
    return HttpResponseRedirect(reverse('modulo:inserir_aula'))

def criar_aula(request, semana_id):
    semana = Semana.objects.get(pk = semana_id)
    aulas = semana.aula_set.all()
    dia=request.POST['dia']
    sala= request.POST['sala']
    hora_inicio= request.POST['hora_inicio']
    hora_fim = time.strftime('09:30')
    try:
        temAula = semana.aula_set.get(dia=request.POST['dia'], hora_inicio=hora_inicio)
    except (KeyError,Aula.DoesNotExist):
        semana.aula_set.create(dia=dia, sala=sala, hora_inicio=hora_inicio, hora_fim=hora_fim)
        return HttpResponseRedirect(reverse('modulo:detalhe_semana', args=semana_id, ))
    else:
        return render(request, 'modulo/horario/detalhe_semana.html',
                      {'semana': semana, 'aulas': aulas, 'error_message': 'Já existe uma aula nesse '})



def procura(request):
    query = request.POST['q']
    questao_list = Questao.objects.filter(Q(questao_texto__icontains=query) | Q(username__icontains=query))
    respostas_list = Resposta.objects.filter(Q(resposta_texto__icontains=query) | Q(resposta_dono__icontains=query))
    return render(request, 'modulo/procura.html', {'questao_list':questao_list , 'respostas_list':respostas_list, 'query':query})

def procura_aluno(request):
    query = request.POST['q']
    alunos = Aluno.objects.all()
    try:
        aluno = Aluno.objects.get(id=query)
    except:
        return render(request, 'modulo/utilizador/darnota.html', {'alunos': alunos, 'error_message':'Não foi encontrado nenhum aluno com esse número.'})
    return render(request, 'modulo/utilizador/darnota_view.html', {'aluno': aluno})