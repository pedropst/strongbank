from datetime import datetime
import pandas as pd
import requests
import streamlit as st
import json

from essentials import get_saldo, get_cliente, get_account_info
from helpers import html_to_fstring


st.set_page_config(page_title="STRONG BANK - Extrato", initial_sidebar_state="collapsed")

def statement_page():
    with open('client/styles/style.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    with open('client/styles/statement_page.html', 'r', encoding='utf8') as f:
        html = f.read()
        html_to_inject = html_to_fstring(html)
        st.markdown(html_to_inject, unsafe_allow_html=True)

    with st.form(key='deposit_form'):
        data_inicial = st.date_input('Data Inicial')
        data_final = st.date_input('Data Final', max_value=datetime.today())
        submit = st.form_submit_button(label='Confirmar')

    if data_inicial and data_final and submit:
        data = {"dta_inicial": data_inicial.strftime(r'%d/%m/%Y'),
                "dta_final": data_final.strftime(r'%d/%m/%Y')}  
        response = requests.post(url='http://127.0.0.1:8000/extrato/', json=data, auth=get_account_info())

        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df = df.drop(['id', 'cliente'], axis=1)
            df = df.rename(columns={'tipo':'TIPO', 'dta_criacao':'DATA', 'valor':'VALOR'})
            st.dataframe(df, width=5000)
            st.legacy_caching.clear_cache()
        else:
            st.write(f'CODE: {response.status_code}')
            st.write(response.json())

    html = """    <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
        <img src='data:image/png;base64,{img_to_bytes()}' style="width: 25%; height: auto;" class="img-fluid">
    </div>"""
    html_to_inject = html_to_fstring(html)
    st.markdown(html_to_inject, unsafe_allow_html=True)

    home_button_html = "<a target='_self' href='http://localhost:8501/home'><input type=button value='Voltar' class='botao_voltar'></a>"
    st.markdown(home_button_html, unsafe_allow_html=True)

    
statement_page()

