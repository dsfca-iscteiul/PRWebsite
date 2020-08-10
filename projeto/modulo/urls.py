from django.conf.urls import url
from . import views

app_name = 'modulo'
urlpatterns = [
 url(r'^$', views.login1, name='login'),
 url(r'^loginview/$', views.loginview, name='loginview'),
 url(r'^logoutview/$', views.logoutview, name='logoutview'),
 url(r'^esqueci_palavra_passe/$', views.esqueci_palavra_passe, name='esqueci_palavra_passe'),
 url(r'^enviar_email/$', views.envia_email, name='enviar_email'),


#Utilizador
 url(r'^utilizador/utilizador/$', views.utilizador, name='utilizador'),
 url(r'^utilizador/alterarpalavrapasse/$', views.alterarpalavrapasse, name='alterarpalavrapasse'),
 url(r'^alterarpasse/$', views.alterarpasse, name='alterarpasse'),
 url(r'^darnota/$', views.darnota, name='darnota'),
 url(r'^darnota_view/$', views.darnota_view, name='darnota_view'),
 url(r'^(?P<aluno_id>[0-9]+)/submeternota/$', views.submeter_nota, name='submeter_nota'),
 url(r'^(?P<aluno_id>[0-9]+)/vernota/$', views.vernota, name='vernota'),
 url(r'^lista_negra/$', views.lista_negra, name='lista_negra'),
 url(r'^(?P<resposta_id>[0-9]+)(?P<nr>[0-9]+)/eliminar_listanegra/$', views.eliminar_listanegra, name='eliminar_listanegra'),
 url(r'^vernota_alunos/$', views.vernota_alunos, name='vernota_alunos'),
 url(r'^utilizador/procura_aluno/$', views.procura_aluno, name='procura_aluno'),


#Forum
 url(r'^forum/(?P<questao_id>[0-9]+)/detalhepostforum/$', views.detalhepostforum, name= 'detalhepostforum'),
 url(r'^enviar/$', views.enviar_pergunta_modulo, name= 'enviar_pergunta_modulo'),
 url(r'^forum/(?P<resposta_id>[0-9]+)/apagar_resposta/$', views.apagar_resposta, name= 'apagar_resposta'),
 url(r'^denunciar_post/(?P<questao_id>[0-9]+)/denunciar_post/$', views.denunciar_post, name= 'denunciar_post'),
 url(r'^(?P<resposta_id>[0-9]+)/denunciar_resposta/$', views.denunciar_resposta, name='denunciar_resposta'),
 url(r'^(?P<questao_id>[0-9]+)/adicionarresposta/$', views.adicionarresposta, name='adicionarresposta'),
 url(r'^(?P<questao_id>[0-9]+)/apagar_questao/$', views.apagar_questao, name='apagar_questao'),
 url(r'^forum/procura/$', views.procura, name='procura'),


 #####     MINISTESTES
 url(r'^conteudos/minitestes/criarminiteste/$', views.criarminiteste, name='criarminiteste'),
 url(r'^(?P<miniteste_id>[0-9]+)/conteudos/minitestes/criarpergunta/$', views.criarpergunta, name='criarpergunta'),
 url(r'^conteudos/minitestes/perguntaminiteste/$', views.criarpergunta, name='perguntaminiteste'),
 url(r'^(?P<miniteste_id>[0-9]+)/adicionarpergunta/$', views.adicionarpergunta, name='adicionarpergunta'),
 url(r'^conteudos/minitestes/(?P<miniteste_id>[0-9]+)/detalheminiteste/$', views.detalheminiteste, name = 'detalheminiteste'),
 url(r'^(?P<cont>[0-9]+)/enviar/$', views.calcularnota, name = 'enviar'),
 url(r'^eliminar_miniteste/$', views.eliminar_miniteste, name = 'eliminar_miniteste'),
 url(r'^eliminar/$', views.eliminar, name = 'eliminar'),
 url(r'^criarminiteste/$', views.criarminiteste, name='criarminiteste'),
 url(r'^adicionarminiteste/$', views.adicionarminiteste, name='adicionarminiteste'),


#Home
 url(r'^index/$', views.index, name='index'),
 url(r'^conteudos/$', views.conteudos, name='conteudos'),
 url(r'^docentes/$', views.docentes, name='docentes'),
 url(r'^forum/$', views.forum, name='forum'),
 url(r'^datasdasavaliacoes/$', views.datasdasavaliacoes, name='datasdasavaliacoes'),
 url(r'^conteudos/minitestes/$', views.minitestes , name='minitestes'),


 #Datas
url(r'^inserir_data/$', views.inserir_data , name='inserir_data'),
url(r'^eliminar_data/$', views.eliminar_data , name='eliminar_data'),
url(r'^apagar_data/$', views.apagar_data , name='apagar_data'),


#####    EXERCICIOS
 url(r'^conteudos/exercicios/$', views.exercicios, name='exercicios'),
 url(r'^eliminar_exercicio/$', views.eliminar_exercicio, name = 'eliminar_exercicio'),
 url(r'^apagar_exercicio/$', views.apagar_exercicio, name = 'apagar_exercicio'),
 url(r'^novo_exercicio/$', views.novo_exercicio, name='novo_exercicio'),
 url(r'^(?P<exercicio_id>[0-9]+)/detalhe_exercicio/$', views.detalhe_exercicio, name = 'detalhe_exercicio'),
 url(r'^(?P<exercicio_id>[0-9]+)/eliminar_ficheiro_exercicio/$',views.eliminar_ficheiro_exercicio, name='eliminar_ficheiro_exercicio'),
 url(r'^(?P<exercicio_id>[0-9]+)/apagar_exercicioficheiro/$',views.apagar_ficheiroexercicio, name='apagar_ficheiroexercicio'),
 url(r'^conteudos/slides/$', views.slides, name='slides'),
 url(r'^conteudos/bibliografia/$', views.bibliografia, name='bibliografia'),


#contudos do slides
 url(r'^(?P<slide_id>[0-9]+)/detalhe_slide/$',views.detalhe_slide, name='detalhe_slide'),
 url(r'^novo_slide/$',views.novo_slide, name='novo_slide'),
 url(r'^eliminar_slide/$',views.eliminar_slide, name='eliminar_slide'),
 url(r'^apagar_slide/$', views.apagar_slide,name='apagar_slide'),
 url(r'^(?P<slide_id>[0-9]+)/eliminar_ficheiro/$',views.eliminar_ficheiro, name='eliminar_ficheiro'),
 url(r'^(?P<slide_id>[0-9]+)/apagar_ficheiro/$', views.apagar_ficheiro,name='apagar_ficheiro'),


#HORARIO
 url(r'^(?P<semana_id>[0-9]+)/horario/$', views.horario, name='horario'),
 url(r'^inserir_aula/$', views.inserir_aula, name='inserir_aula'),
 url(r'^(?P<semana_id>[0-9]+)/detalhe_semana/$', views.detalhe_semana, name='detalhe_semana'),
 url(r'^criar_semana/$', views.criar_semana, name='criar_semana'),
 url(r'^(?P<semana_id>[0-9]+)/criar_aula/$', views.criar_aula, name='criar_aula'),

]