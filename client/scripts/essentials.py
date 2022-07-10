import requests
import json

ACCOUNT_INFO = ''
with open('client/cookie.json') as json_file:
    ACCOUNT_INFO = json.load(json_file)

LOGIN = ACCOUNT_INFO['conta_logada']
SENHA = ACCOUNT_INFO['senha_logada']

def get_account_info():
    with open('client/cookie.json') as json_file:
        ACCOUNT_INFO = json.load(json_file)
    return ACCOUNT_INFO['conta_logada'], ACCOUNT_INFO['senha_logada']

def get_cliente():
    return requests.get(url='http://127.0.0.1:8000/cliente/', auth=get_account_info()).json()

def get_saldo():
    return requests.get(url='http://127.0.0.1:8000/saldo/', auth=get_account_info()).json()['Seu saldo é: ']
