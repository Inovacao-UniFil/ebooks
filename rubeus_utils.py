
import os
import requests
import json

#Envia Lead para Rubeus
def send_lead_rubeus(name, email, phone, grauInstrucao, ebook):
    origin = os.environ.get('RUBEUS_ORIGEM_EBOOK')
    token = os.environ.get('RUBEUS_TOKEN_EBOOK')
    #Cadastrar usuario no sistema
    url = os.environ.get('RUBEUS_URL')+"/Contato/cadastro"
    data = {
        "origem": origin,
        "nome": name,
        "telefonePrincipal": phone,
        "emailPrincipal": email,
        "telefone": [
            phone
        ],
        "grauInstrucao": grauInstrucao,
        "email": [
            email
        ],
        "token": token,
    }
    response = requests.post(url=url,data=data).json()
    print(response)
    print(response['dados'])
    #Criar evento de isncrição do curso
    url = os.environ.get('RUBEUS_URL')+"/Evento/cadastro"
    data = {
        "tipo": 598,
        "pessoa" : {
            "id": response['dados']
        },
        "descricao":"Increveu-se campanha Ebook.",
        "origem": origin,
        "camposPersonalizados" : { "campopersonalizado_97_compl_proc": ebook },
        "token": token
    }
    print(data)
    response = requests.post(url=url,data=json.dumps(data),headers={"Content-Type":"application/json"}).json()
    print(response)
    return "Ok"
