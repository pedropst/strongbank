from datetime import datetime
import pandas as pd
import requests
import streamlit as st

from essentials import get_saldo, get_cliente, get_cartao, get_account_info
from helpers import html_to_fstring_com_iterador, html_to_fstring


st.set_page_config(page_title="STRONG BANK - Cartões", initial_sidebar_state="collapsed")

def card_page():
    with open('client/styles/style.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    with open('client/styles/card_3d.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    with open('client/styles/card.html', 'r', encoding='utf8') as f:
        html = f.read()
        html_to_inject = html_to_fstring(html)
        st.markdown(html_to_inject, unsafe_allow_html=True)
   
    _, b, c, _, _ = st.columns(5)
    # with b:
    #     data = {"numeracao":get_cartao()['numeracao']} 
    #     bloquear = st.select_slider('Bloqueado', options=['SIM', 'NÃO'], value='NÃO')
    #     response = requests.get(url='http://127.0.0.1:8000/cartao/', json=data, auth=get_account_info())
    #     # breakpoint()
    #     id = response.json()['id']
    #     data = response.json()

    #     if bloquear == 'SIM':
    #         data['bloqueado'] = True
    #         response = requests.patch(url=f'http://127.0.0.1:8000/cartao/{id}', json=data, auth=get_account_info())
    #         breakpoint()
    #     else:
    #         data['bloqueado'] = False
    #         response = requests.patch(url=f'http://127.0.0.1:8000/cartao/{id}', json=data, auth=get_account_info())

    with c:
        data = {"numeracao":get_cartao()['numeracao']}  
        response = requests.get(url='http://127.0.0.1:8000/fatura/', json=data, auth=get_account_info())
        data = response.json()['FATURAS']
        parcelas = response.json()['PARCELAS']
        data = sorted(data, key=lambda x: datetime(x['ano_ref'], x['mes_ref'], 1))
        options = [f"{x['mes_ref']}/{x['ano_ref']}" for x in data]
        fatura = st.selectbox('Fatura', options=options if data != {} else ['SEM FATURA'])

    if fatura != None:
        index = options.index(fatura)
        parcelas = [p for p in parcelas if p['fatura'] == data[index]['id']]
        # breakpoint()
        df = pd.DataFrame(parcelas)
        df = df.drop(['id', 'fatura'], axis=1)
        df = df.rename(columns={'descricao':'DESCRIÇÃO', 'valor':'VALOR', 'dta_criacao': 'DATA'})
        df = df[['DATA', 'DESCRIÇÃO', 'VALOR']]
        st.dataframe(df, width=1200)
    
    html = """    <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
        <img src='data:image/png;base64,{img_to_bytes()}' style="width: 25%; height: auto;" class="img-fluid">
    </div>"""
    html_to_inject = html_to_fstring(html)

    st.markdown(html_to_inject, unsafe_allow_html=True)

    home_button_html = "<a target='_self' href='http://localhost:8501/home'><input type=button value='Voltar' class='botao_voltar'></a>"
    st.markdown(home_button_html, unsafe_allow_html=True)


card_page()

