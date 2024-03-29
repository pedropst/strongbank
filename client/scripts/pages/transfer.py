import requests
import streamlit as st

from essentials import get_saldo, get_customer, get_account_info
from helpers import html_to_fstring


st.set_page_config(page_title="STRONG BANK", initial_sidebar_state="collapsed", page_icon=FR"client\resources\images\logo_icon.png")

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
        receiver_account_number = st.text_input('Número:')
        receiver_document = st.text_input('CPF Destinatário:')
        description = st.text_input('Descrição:')
        password = st.text_input('Senha:', type='password')
        submit = st.form_submit_button(label='Confirmar')

    html = """    <div style="display: flex; justify-content: center; align-items: center; margin: 20px;">
        <img src='data:image/png;base64,{img_to_bytes()}' style="width: 25%; height: auto;" class="img-fluid">
        </div>"""
    html_to_inject = html_to_fstring(html)
    st.markdown(html_to_inject, unsafe_allow_html=True)

    if receiver_document and value and submit and receiver_account_number and receiver_branch and password:
        data = {
                    "valor": value,
                    "doc_destinatario":receiver_document,
                    "numero": receiver_account_number,
                    "agencia": receiver_branch,
                    "senha": password,
                    "descricao": description
               }
        response = requests.post(url='http://127.0.0.1:8000/transferir/', json=data, auth=get_account_info())

        if response.status_code == 200:
            st.legacy_caching.clear_cache()
            st.experimental_rerun()
        else:
            st.write(f'CODE: {response.status_code}')
            st.write(response.json())

    home_button_html = "<a target='_self' href='http://localhost:8501/home'><input type=button value='Voltar' class='botao_voltar'></a>"
    st.markdown(home_button_html, unsafe_allow_html=True)


transfer_page()

