import requests
import streamlit as st

from essentials import get_saldo, get_cliente, get_account_info
from helpers import html_to_fstring


st.set_page_config(page_title="STRONG BANK", initial_sidebar_state="collapsed")

def transfer_page():
    with open('client/styles/style.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    with open('client/styles/transfer_page.html', 'r', encoding='utf8') as f:
        html = f.read()
        html_to_inject = html_to_fstring(html)
        st.markdown(html_to_inject, unsafe_allow_html=True)

    with st.form(key='transfer_form'):
        value = st.number_input('Valor:')
        receiver_branch = st.text_input('Agência:')
        receiver_document = st.text_input('CPF Destinatário:')
        description = st.text_input('Descrição:')
        password = st.text_input('Senha:', type='password')
        submit = st.form_submit_button(label='Confirmar')

    if receiver_document and value and submit:
        data = {
                "valor": value,
                "doc_destinatario": receiver_document
            }
        requests.post(url='http://127.0.0.1:8000/transferir/', json=data, auth=get_account_info())

        st.legacy_caching.clear_cache()
        st.experimental_rerun()

    home_button_html = "<a target='_self' href='http://localhost:8501/home'><input type=button value='Voltar'></a>"
    st.markdown(home_button_html, unsafe_allow_html=True)


transfer_page()

