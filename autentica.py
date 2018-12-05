#!/usr/bin/env python3
# encoding: utf-8

import cgi
import json
import requests
import cgitb
import sys
import codecs

cgitb.enable()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

urls = { 'token':'https://suap.ifrn.edu.br/api/v2/autenticacao/token/', 'dados':'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/'}


## --------------------------------------------------------------------------------------------
# Funções do SUAP
## --------------------------------------------------------------------------------------------

def getToken(autenticacao): # Retorna o token para acesso ao SUAP.
	response = requests.post(urls['token'], data=autenticacao)
	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))['token']
	return None

def getInformacoes(cabecalho): # Retorna os dados utilizando o token.
	response = requests.get(urls['dados'], headers=cabecalho)
	if response.status_code == 200:
		return response.content.decode('utf-8')
	return None

def autentica(login,senha):
	autenticacao = { 'username': login, 'password': senha }
	token = getToken(autenticacao)
	if token == None: return None
	cabecalho = {'Authorization': 'JWT {0}'.format(token)}
	informacoes = getInformacoes(cabecalho)
	if informacoes == None: return None
	return json.loads(informacoes)

## --------------------------------------------------------------------------------------------
# Funcão para inserir os dados no exibe.html de acordo com o vínculo
## --------------------------------------------------------------------------------------------
def gerarHTML(informacoes):
	matricula = informacoes['matricula']
	nome = informacoes['vinculo']['nome']
	email = informacoes['email']
	campus = informacoes['vinculo']['campus']
	vinculo = informacoes['tipo_vinculo']
	foto = 'https://suap.ifrn.edu.br' + informacoes['url_foto_75x100']
	with open('exibe.html', 'rb') as arq: exibe = arq.read().decode('utf-8')
	exibe = 'Content-type: text/html\n\n' + exibe
	exibe = exibe.replace('val_foto',foto)
	exibe = exibe.replace('val_matricula',matricula)
	exibe = exibe.replace('val_nome',nome)
	exibe = exibe.replace('val_email',email)
	exibe = exibe.replace('val_campus',campus)
	exibe = exibe.replace('val_vinculo',vinculo)
	if vinculo == 'Servidor':
		diretoria = informacoes['vinculo']['setor_suap']
		discingresso = informacoes['vinculo']['disciplina_ingresso']
		dados = '''
				<label for="diretoria">Diretoria: {0}</label>
				<input type="hidden" id="diretoria" name="diretoria" value="{0}">
				<br />
				<label for="discingresso">Disciplina de Ingresso: {1}</label>
				<input type="hidden" id="discingresso" name="discingresso" value="{1}">
				<br />
				'''.format(diretoria,discingresso)
		exibe = exibe.replace('<!--servidor-->',dados)
	if vinculo == 'Aluno':
		curso = informacoes['vinculo']['curso']
		dados = '''
				<label for="curso">Curso: {0}</label>
				<input type="hidden" id="curso" name="curso" value="{0}">
				<br />
				'''.format(curso)
		exibe = exibe.replace('<!--aluno-->',dados)
	return exibe
## --------------------------------------------------------------------------------------------

## --------------------------------------------------------------------------------------------
# MAIN
## --------------------------------------------------------------------------------------------
form = cgi.FieldStorage()
matricula = form.getvalue('matricula')
senha = form.getvalue('senha')


informacoes = autentica(matricula, senha)


if informacoes == None:
	print('Content-type: text/html\n')
	msg ='<br /><font color="red">Não foi possível realizar o login no SUAP. Por obséquio, tente novamente.</font>'
	with open('index.html', 'rb') as arq: print(arq.read().decode('utf-8').replace('<!--msg-->',msg))
else:
	html = gerarHTML(informacoes)
	print(html)

## --------------------------------------------------------------------------------------------
