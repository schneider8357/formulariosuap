#!/usr/bin/env python3 
import cgi
import json
import requests
import psycopg2

import cgitb
cgitb.enable()

urls = { 'token':'https://suap.ifrn.edu.br/api/v2/autenticacao/token/', 'dados':'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/'}

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

form = cgi.FieldStorage()
matricula = form.getvalue("user")
senha = form.getvalue("pass")


informacoes = autentica(matricula.encode('utf-8'), senha.encode('utf-8'))

print("Content-type: text/html\n\n")
print("<html><body>")
if informacoes == None:
	print("<h1>Não foi possível realizar o login no SUAP. Por obséquio, tente novamente.</h1>")
else:
	print ("<h1>{}</h1>".format(informacoes['vinculo']['situacao_sistemica']))
print ("</body></html>")
