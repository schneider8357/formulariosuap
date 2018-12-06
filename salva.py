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
strConexaoAluno = "dbname=aluno user=postgres host=localhost password=aluno"
strConexaoServidor = "dbname=servidor user=postgres host=localhost password=aluno"
strCreateAluno = "create table aluno (alu_matricula bigint not null primary key, " \
									 "alu_nome varchar(100), "\
									 "alu_email varchar(200) "\
									 "alu_campus varchar(50) "\
									 "alu_curso varchar(200))" 


def db_exists(datname):
	exists = False
	try:
		strSQL = "select datname from pg_database where datname='{}'".format(datname)
		con = psycopg2.connect(strConexaoPostgres)
		cur = con.cursor()
		cur.execute(strSQL)
		if nomeTabela == cur.fetchone()[0]: exists = True
		cur.close()
	except psycopg2.Error as e:
		print (e)
	return exists

def table_exists(datname, tablename):
	exists = False
	try:
		strSQL = "select datname from pg_table where tableowner='{}' tablename='{}'".format(datname,tablename)
		con = psycopg2.connect(strConexaoPostgres)
		cur = con.cursor()
		cur.execute(strSQL)
		if nomeTabela == cur.fetchone()[0]: exists = True
		cur.close()
	except psycopg2.Error as e:
		print (e)
	return exists

def db_create(datname):
	try:
		strSQL = "create database {}".format(datname)
		con = psycopg2.connect(strConexaoPostgres)
		cur = con.cursor()
		cur.execute(strSQL)
		if nomeTabela == cur.fetchone()[0]: exists = True
		cur.close()
	except psycopg2.Error as e:
		print (e)

def table_create(datname,tipo):
	if tipo == "Aluno":
		try:
			con = psycopg2.connect(strConexaoAluno)
			cur = con.cursor()
			cur.execute(strCreateAluno)
			cur.close
		except psycopg2.Error as e:
			print (e)
	if tipo == "Servidor"


def main():
	form = cgi.FieldStorage()
	matricula = form.getvalue("matricula")
	nome = form.getvalue("nome")
	email = form.getvalue("email")
	campus = form.getvalue("campus")
	vinculo = form.getvalue("vinculo")


	print("Content-type: text/html\n\n")
	if db_exists("db_suap"):
		if table_exists("db_suap",vinculo):
			print("a tabela aluno existe!")
		else:
			table_create("db_suap",vinculo)
	else:
		db_create("db_suap")

if __name__ == "__main__": main()
