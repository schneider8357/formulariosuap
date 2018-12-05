#!/usr/bin/env python3
# encoding: utf-8

import cgi
import cgitb
import sys
import codecs
import psycopg2

cgitb.enable()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

strConexao = 'dbname=postgres user=postgres host=localhost'

def dat_exists(nomeTabela):
	exists = False
	try:
		strSQL = "select datname from pg_database where datname='{}'".format(nomeTabela)
		con = psycopg2.connect(strConexao+' password=aluno')
		cur = con.cursor()
		cur.execute(strSQL)
		if nomeTabela == cur.fetchone()[0]: exists = True
		cur.close()
	except psycopg2.Error as e:
		print (e)
	return exists

def createTable(tipo):
	if tipo == aluno: strSQL = ''

form = cgi.FieldStorage()
matricula = form.getvalue('matricula')
nome = form.getvalue('nome')
email = form.getvalue('email')
campus = form.getvalue('campus')
vinculo = form.getvalue('vinculo')


print('Content-type: text/html\n\n')
exists = dat_exists('teste')
if exists: print('O banco teste existe.')
