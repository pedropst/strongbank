from datetime import datetime
import pandas as pd
import requests
import streamlit as st
import json

from essentials import get_saldo, get_cliente, get_cartao, get_account_info
from helpers import html_to_fstring_com_iterador, html_to_fstring


st.set_page_config(page_title="STRONG BANK - Cartões", initial_sidebar_state="collapsed", page_icon=FR"client\resources\images\logo_icon.png")

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
   
    with st.expander('Pagar com crédito:'):
        with st.form('credit_payment_form'):
            value_c = st.number_input(label='Valor')
            quantity_c = st.number_input(label='Parcelas', step=1)
            description_c = st.text_input(label='Descrição')
            submit_c = st.form_submit_button(label='Confirmar')

    with st.expander('Pagar com débito:'):
        html = """<p style="color:white; margin-bottom: 10px;">Seu saldo em conta é: R$ {get_saldo()}</p>"""
        html_to_inject = html_to_fstring(html)
        st.markdown(html_to_inject, unsafe_allow_html=True)

        with st.form('debit_payment_form'):
            value_d = st.number_input(label='Valor')
            description_d = st.text_input(label='Descrição')
            submit_d = st.form_submit_button(label='Confirmar')

    with st.expander('Faturas'):
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

    if value_c and quantity_c and submit_c:
        data = {"valor":value_c, "descricao":description_c, "parcelas":quantity_c}
        response = requests.post(url='http://127.0.0.1:8000/pagarcredito/', json=data, auth=get_account_info())
        if response.status_code == 200:
            st.legacy_caching.clear_cache()
            st.experimental_rerun()
        else:
            st.write(response.json())
    elif value_d and submit_d:
        data = {"valor":value_d, "descricao":description_d}
        response = requests.post(url='http://127.0.0.1:8000/pagardebito/', json=data, auth=get_account_info())
        if response.status_code == 200:
            st.legacy_caching.clear_cache()
            st.experimental_rerun()
        else:
            st.write(response.json())
    
    
    #         _, b, c, _, _ = st.columns(5)
    # # with b:
    # #     data = {"numeracao":get_cartao()['numeracao']} 
    # #     bloquear = st.select_slider('Bloqueado', options=['SIM', 'NÃO'], value='NÃO')
    # #     response = requests.get(url='http://127.0.0.1:8000/cartao/', json=data, auth=get_account_info())
    # #     # breakpoint()
    # #     id = response.json()['id']
    # #     data = response.json()

    # #     if bloquear == 'SIM':
    # #         data['bloqueado'] = True
    # #         response = requests.patch(url=f'http://127.0.0.1:8000/cartao/{id}', json=data, auth=get_account_info())
    # #         breakpoint()
    # #     else:
    # #         data['bloqueado'] = False
    # #         response = requests.patch(url=f'http://127.0.0.1:8000/cartao/{id}', json=data, auth=get_account_info())

    
    html = """    <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
        <img src='data:image/png;base64,{img_to_bytes()}' style="width: 25%; height: auto;" class="img-fluid">
    </div>"""
    html_to_inject = html_to_fstring(html)

    st.markdown(html_to_inject, unsafe_allow_html=True)

    home_button_html = "<a target='_self' href='http://localhost:8501/home'><input type=button value='Voltar' class='botao_voltar'></a>"
    st.markdown(home_button_html, unsafe_allow_html=True)


def register_card_page():
    with open('client/styles/style.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    with open('client/styles/register_card_page.html', 'r', encoding='utf8') as f:
        html = f.read()
        html_to_inject = html_to_fstring(html)
        st.markdown(html_to_inject, unsafe_allow_html=True)

    with st.form(key='card_form'):
        vencimento = st.text_input(label='Dia do vencimento:')
        limite = st.text_input(label='Limite:')
        submit = st.form_submit_button(label='Confirmar')

    if vencimento and limite and submit:
        data = {
                    "dia_vencimento": vencimento,
                    "tipo":"1",
                    "limite_total":limite
               }


        response = requests.post(url='http://127.0.0.1:8000/cartao/', json=data, auth=get_account_info())

        if response.status_code == 201:
            st.legacy_caching.clear_cache()
            st.experimental_rerun()
        else:
            st.write(response.json())

    html = """    <div style="display: flex; justify-content: center; align-items: center; margin: 20px;">
        <img src='data:image/png;base64,{img_to_bytes()}' style="width: 25%; height: auto;" class="img-fluid">
    </div>"""
    html_to_inject = html_to_fstring(html)

    st.markdown(html_to_inject, unsafe_allow_html=True)

try:
    get_cartao()
    card_page()
except requests.JSONDecodeError:
    register_card_page()

