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
		strSQL = "create database db_suap"
		con = psycopg2.connect(strConexaoPostgres)
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
	


def main():
	print("Content-type: text/html\n\n")
	if db_exists():
		print("O banco existe!")
	else:
		print("Criando o banco...")
		db_create()
	if table_exists():
		print("A tabela usuario existe!")
	else:
		print("Criando tabela usuario...")
		table_create()
	if user_exists(matricula):
		print("O usuário já está cadastrado.")
	else:
		print("Inserindo usuário...")
		user_insert()
	

if __name__ == "__main__": main()
