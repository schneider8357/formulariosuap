#!/usr/bin/env python3
# encoding: utf-8

import cgi
import cgitb
import sys
import codecs
import psycopg2

cgitb.enable()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

strConexaoPostgres = "dbname=postgres user=postgres host=localhost password=aluno"
strConexaoSuap = "dbname=db_suap user=postgres host=localhost password=aluno"
strCreateAluno = "create table usuario ( matricula bigint not null primary key, " \
										"nome varchar(100), "\
										"email varchar(200), "\
										"campus varchar(50), "\
										"curso varchar(200), "\
										"vinculo varchar(50), "\
										"foto varchar(200))" 

form = cgi.FieldStorage()
matricula = form.getvalue("matricula")
nome = form.getvalue("nome")
email = form.getvalue("email")
vinculo = form.getvalue("vinculo")
foto = form.getvalue("foto")
if vinculo == "Aluno":
	campus = form.getvalue("campus")
	curso = form.getvalue("curso")
elif vinculo == "Servidor":
	campus = form.getvalue("setor")
	curso = form.getvalue("discingresso")
else:
	pass

def db_exists():
	exists = False
	try:
		strSQL = "select datname from pg_database where datname='db_suap'"
		con = psycopg2.connect(strConexaoPostgres)
		cur = con.cursor()
		cur.execute(strSQL)
		if cur.fetchone(): exists = True
		cur.close()
		con.close()
	except psycopg2.Error as e:
		print (e)
	return exists

def table_exists():
	exists = False
	try:
		strSQL = "select relname from pg_class where relname='usuario'"
		con = psycopg2.connect(strConexaoSuap)
		cur = con.cursor()
		cur.execute(strSQL)
		if cur.fetchone(): exists = True
		cur.close()
		con.close()
	except psycopg2.Error as e:
		print (e)
	return exists

def user_exists(matricula):
	exists = False
	try:
		strSQL = "select matricula from usuario where matricula='{}'".format(matricula)
		con = psycopg2.connect(strConexaoSuap)
		cur = con.cursor()
		cur.execute(strSQL)
		if cur.fetchone(): exists = True
		cur.close()
		con.close()
	except psycopg2.Error as e:
		print (e)
	return exists

def db_create():
	try:
		from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
		strSQL = "create database db_suap"
		con = psycopg2.connect(strConexaoPostgres)
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		cur.execute(strSQL)
		cur.close()
		con.close()
	except psycopg2.Error as e:
		print (e)

def table_create():
	try:
		con = psycopg2.connect(strConexaoSuap)
		cur = con.cursor()
		cur.execute(strCreateAluno)
		cur.close()
		con.commit()
		con.close()
	except psycopg2.Error as e:
		print (e)

def user_insert():
	conn = psycopg2.connect(strConexaoSuap)
	cur = conn.cursor()
	strSQLInsereDados = "insert into usuario values ({0}, '{1}', '{2}','{3}','{4}','{5}','{6}')".format(matricula,nome,email,campus,curso,vinculo,foto)
	cur.execute(strSQLInsereDados)
	conn.commit()
	conn.close()
	
def gerarHTML(exists):
	with open('exibe.html', 'rb') as arq: exibe = arq.read().decode('utf-8')
	exibe = 'Content-type: text/html\n\n' + exibe
	exibe = exibe.replace('val_foto',foto)
	exibe = exibe.replace('val_matricula',matricula)
	exibe = exibe.replace('val_nome',nome)
	exibe = exibe.replace('val_email',email)
	exibe = exibe.replace('val_campus',campus)
	exibe = exibe.replace('val_vinculo',vinculo)
	if vinculo == 'Servidor':
		dados = '''
				<label for="setor">Setor SUAP: {0}</label>
				<input type="hidden" id="setor" name="setor" value="{0}">
				<br />
				<label for="discingresso">Disciplina de Ingresso: {1}</label>
				<input type="hidden" id="discingresso" name="discingresso" value="{1}">
				<br />
				'''.format(campus,curso)
		exibe = exibe.replace('<!--servidor-->',dados)
	if vinculo == 'Aluno':
		dados = '''
				<label for="campus">Campus: {0}</label>
				<input type="hidden" id="campus" name="campus" value="{0}">
				<br />
				<label for="curso">Curso: {1}</label>
				<input type="hidden" id="curso" name="curso" value="{1}">
				<br />
				'''.format(campus,curso)
		exibe = exibe.replace('<!--aluno-->',dados)
	button = '<button type="submit">Salvar</button>'
	if exists: msg = '<font color="red">O usuário já está cadastrado!</font>'
	else: msg = '<font color="green">Dados salvos com sucesso!</font>'
	exibe = exibe.replace(button,msg)
	return exibe

def main():
	if db_exists():
		#print("O banco existe!")
		pass
	else:
		#print("Criando o banco...")
		db_create()
	if table_exists():
		#print("A tabela usuario existe!")
		pass
	else:
		#print("Criando tabela usuario...")
		table_create()
	if user_exists(matricula):
		#print("O usuário já está cadastrado.")
		print(gerarHTML(1))
	else:
		#print("Inserindo usuário...")
		user_insert()
		print(gerarHTML(0))
	

if __name__ == "__main__": main()
