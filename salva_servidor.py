#!/usr/bin/env python3
# encoding: utf-8

import cgi
import json
import cgitb
import sys
import codecs
import psycopg2

cgitb.enable()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


informacoes = cgi.FieldStorage()
nome = form.getvalue('nome')
email = form.getvalue('email')
campus = form.getvalue('campus')
vinculo = form.getvalue('vinculo')
diretoria = form.getvalue('diretoria')
discingresso = form.getvalue('discingresso')


print('Content-type: text/html\n\n')
print('Matricula: {}').format(matricula)
