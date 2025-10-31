from flask import Flask, render_template, request, redirect, send_from_directory
from pathlib import Path
import os
import psycopg2
from dotenv import load_dotenv
import requests
import json
from unidecode import unidecode
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone, time, date
from flask import render_template
from rubeus_utils import send_lead_rubeus
from gmail_utils import send_email, define_student_email

load_dotenv()
app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_ PASSWORD')

#Encriptar dados usando uma chave do ambiente
def encrypt(value):
    encrypted_value = ""
    key_index = 0
    value = unidecode(value)
    key = os.environ.get('ENCRYPT_KEY')
    for value_index in range(len(value)):
        char_value = (ord(value[value_index]) + ord(key[key_index]))
        if char_value > 126:
            char_value -= (127-32)
        if char_value < 32:
            char_value += 32
        char = chr(char_value) 
        encrypted_value+=char
        key_index+=1
        if key_index >= len(key): key_index=0
    return encrypted_value.encode('utf8','surrogateescape').decode('utf8','surrogateescape')

#Desencriptar dados usando uma chave do ambiente
def decrypt(value):
    encrypted_value = ""
    key_index = 0
    value = value
    key = os.environ.get('ENCRYPT_KEY')
    for value_index in range(len(value)):
        char_value = (ord(value[value_index]) - ord(key[key_index]))
        if char_value < 32:
            char_value += (127-32)
        if char_value < 32:
            char_value += (32)
        char = chr(char_value) 
        encrypted_value+=char
        key_index+=1
        if key_index >= len(key): key_index=0
    return encrypted_value

app.config['static_folder'] = BASE_DIR / 'static'
app.config['UPLOAD_FOLDER'] = BASE_DIR / 'static/pdf' 
#Conectar banco
def get_db_connection():
    conn = psycopg2.connect(hostaddr=os.environ.get('DB_HOST'),
                            port=os.environ.get('DB_PORT'),
                            user=os.environ.get('UNFL_USERNAME'),
                            password=os.environ.get('UNFL_PASSWORD'),
                            database=os.environ.get('UNFL_NAME'))
    return conn

@app.route("/")
def main():
    #Conectar Banco
    print(app.config['UPLOAD_FOLDER'])
    conn = get_db_connection()
    cur = conn.cursor()
    #Criar tabela se não existe
    cur.execute("CREATE TABLE IF NOT EXISTS unifilista.ebooks (id serial PRIMARY KEY, nome text, email text, telefone text, schoollv integer, codigo smallserial, horario timestamp);")
    conn.commit()
    #Encerrar conexao
    cur.close()
    conn.close()
    return render_template('ebook.html')

@app.route("/consultar")
def consultar():
    return render_template('consultar.html')

#Adiciona o usuario ao banco de dados
@app.route("/send_data", methods=["POST"])
def send_data():
    data = request.json
    email = (data.get("email").lower())
    nome = encrypt(data.get("nome"))
    telefone = encrypt(data.get("telefone"))
    schoollv= data.get("escolaridade")
    ebookFile = data.get("ebookFile")
    #Conectar Banco
    print("Conectar")
    conn = get_db_connection()
    print("Conectado")
    cur = conn.cursor()
    #Criar tabela se não existe
    cur.execute("CREATE TABLE IF NOT EXISTS unifilista.ebooks (id serial PRIMARY KEY, nome text, email text, telefone text, schoollv integer, codigo smallserial, horario timestamp);")    #Verificar se aluno é duplicado
    cur.execute(f"SELECT * FROM ebooks WHERE email = %s;", [email])
    get = cur.fetchone()
    print(get)
    if get:
        #Aluno duplicado
        cur.close()
        conn.close()
        msg = f"Aluno já cadastrou."
    else:
        
        #redirection_url = Flask.url_for(app,endpoint='success')+f"?comprovante=Encerrada&new=True"
        #return {
        #    "success": f"Not Permited.",
        #    "codigo": f"NONE",
        #    "new": True,
        #    "url": redirection_url
        #    }
        #Inserir dados Aluno
        cur.execute(f"INSERT INTO ebooks (nome, email, telefone, schoollv, horario) VALUES" + 
                    f"(%s,%s,%s,%s, CURRENT_TIMESTAMP);",[nome,email,telefone,schoollv])
        conn.commit()
        #Receber Codigo de confirmacao conexao
        cur.execute(f"SELECT * FROM ebooks WHERE email = %s;", [email])
        get = cur.fetchone()
        cur.close()
        conn.close()
        msg = "Sucesso."
        #Enviar para CRM
    crm_nome = data.get("nome").upper()
    crm_email = data.get("email").upper()
    crm_telefone = data.get("telefone")
    send_lead_rubeus(crm_nome,crm_email,crm_telefone,schoollv)
    #Redirecionar
    downloadurl = "http://127.0.0.1:5000" + app.url_for('download') + f"?filename={ebookFile}" 
    message = define_student_email(downloadurl )
    attachment = ebookFile
    send_email("Ebooks UniFil", message, attachment, crm_email)
    return { 
        "success": msg,
        "downloadurl" : downloadurl 
        }
 
@app.route('/download',methods=['GET','POST'])
def download():
    filename = request.args.get('filename')
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
 
#Popula o Excel de usuarios que se inscreveram
#@app.route("/getdata")
def getdata():
    schooldict = {
        "6":	"Ensino médio incompleto",
        "7":	"Ensino médio completo",
        "8":	"Educação superior incompleto",
        "9":	"Educação superior completo"
    }
    comp = request.args.get("comprovante") 
    print(comp)
    #Conectar Banco
    print("Conectar")
    conn = get_db_connection()
    print("Conectado")
    cur = conn.cursor()
    #Verificar se aluno é duplicado
    #cur.execute(f"SELECT * FROM ebooks WHERE codigo = %s;", [comp])
    cur.execute(f"SELECT * FROM ebooks")
    student_list = []
    all = cur.fetchall()
    for get in all:
        id = get[0]
        name = decrypt(get[1])
        email = (get[2])
        telefone = decrypt(get[3])
        schoollv = get[4]
        schoollv = schooldict[schoollv]
        code = get[5]
        data = [name,email,telefone,code]
        student_list.append(data)
    df = pd.DataFrame(data=student_list,columns=["Nome","Email","Telefone","Escolaridade","Código de Confirmação","Data de cadastro"])
    Path(BASE_DIR / "ebooks.xlsx").touch()
    print(BASE_DIR / "ebooks.xlsx")
    df.to_excel(excel_writer = BASE_DIR / "ebooks.xlsx")
    cur.close()
    conn.close()
    return render_template('sucesso.html')

@app.route('/consult', methods=["POST"])
def consult():
    #Conectar Banco
    print("Conectar")
    conn = get_db_connection()
    print("Conectado")
    cur = conn.cursor()
    data = request.json
    if(data.get("comprovante")):
        comprovante = data.get("comprovante")
        codigo = int(comprovante[4:])
        cur.execute(f"SELECT * FROM ebooks WHERE codigo = %s;", [codigo])
    else:
        email = (data.get("email").lower())
        telefone = encrypt(data.get("telefone"))  
        cur.execute(f"SELECT * FROM ebooks WHERE email = %s AND telefone = %s;", [email, telefone])
    get = cur.fetchone()
    if get:
        #Aluno duplicado
        codigo = get[5]
        cur.close()
        conn.close()
        redirection_url = Flask.url_for(app,endpoint='success')+f"?comprovante=CONF{str(codigo).zfill(6)}"
        print(redirection_url)
        return {
            "success": f"Aluno já cadastrou.",
            "codigo": f"CONF{str(codigo).zfill(6)}",
            "url": redirection_url
            }
    else:
        redirection_url = Flask.url_for(app,endpoint='failed')
        return {
            "success": f"Aluno não encontrado.",
            "url": redirection_url
            }

        
#@app.route('/test_rubeus')
def test_rubeus():
    return send_lead_rubeus("John Dude","test@test.com","43999999999")

#Rota de sucesso
@app.route("/success")
def success():
    return render_template('sucesso.html')

@app.route('/failed')
def failed():
    return render_template('failed.html')

