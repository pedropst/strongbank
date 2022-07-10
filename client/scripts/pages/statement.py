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
        df = pd.DataFrame.from_dict(response.json(), orient='index', columns=['Descrição'])
        st.dataframe(df)
        st.legacy_caching.clear_cache()

    home_button_html = "<a target='_self' href='http://localhost:8501/home' style='padding:20px'><input type=button value='Voltar'></a>"
    st.markdown(home_button_html, unsafe_allow_html=True)


statement_page()

