import requests
import json

ACCOUNT_INFO = ''
with open('client/cookie.json') as json_file:
    ACCOUNT_INFO = json.load(json_file)

LOGIN = ACCOUNT_INFO['username']
SENHA = ACCOUNT_INFO['password']

def get_account_info():
    with open('client/cookie.json') as json_file:
        ACCOUNT_INFO = json.load(json_file)
    return ACCOUNT_INFO['username'], ACCOUNT_INFO['password']

def get_cliente():
    return requests.get(url='http://127.0.0.1:8000/cliente/', auth=get_account_info()).json()

def get_cartao():
    return requests.get(url='http://127.0.0.1:8000/cartao/', auth=get_account_info()).json()
    
def get_saldo():
    return f"{requests.get(url='http://127.0.0.1:8000/saldo/', auth=get_account_info()).json():,.2f}".replace(',', '*').replace('.',',').replace('*','.')
