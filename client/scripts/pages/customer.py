import json
import streamlit as st
import requests
from essentials import get_account_info

from helpers import html_to_fstring


st.set_page_config(page_title="STRONG BANK - Customer Create", initial_sidebar_state="collapsed")

def account_create_page():
    with open('client/styles/style.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    with open('client/styles/customer_page.html', 'r', encoding='utf8') as f:
        html = f.read()
        html_to_inject = html_to_fstring(html)
        st.markdown(html_to_inject, unsafe_allow_html=True)

    with st.form(key='register_form'):
        nome = st.text_input(label='Nome:')
        endereco = st.text_input(label='Endereço:')
        celular = st.text_input(label='Celular:')
        documento = st.text_input(label='Número doc.:')
        tipo = st.select_slider(label='Tipo de conta:', options=['PF', 'PJ'])
        submit = st.form_submit_button(label='Confirmar')

    if nome and endereco and celular and documento and tipo and submit:
        data = {
                    "nome": nome,
                    "endereco": endereco,
                    "celular": celular,
                    "cpf": documento if tipo == "PF" else "",
                    "cnpj": documento if tipo == "PJ" else "",
                    "tipo": tipo
                }

        response = requests.post(url='http://127.0.0.1:8000/cliente/', json=data, auth=get_account_info())
        # breakpoint()
        if response.status_code == 201:
            st.markdown("<a target='_self' href='http://localhost:8501/account' class='botao_voltar' style='position:absolute; right:50px'><input type=button value='Avançar'></a>", unsafe_allow_html=True)
        else:
            st.write(response.json())

    html = """    <div style="display: flex; justify-content: center; align-items: center; margin: 20px;">
        <img src='data:image/png;base64,{img_to_bytes()}' style="width: 25%; height: auto;" class="img-fluid">
    </div>"""
    html_to_inject = html_to_fstring(html)

    st.markdown(html_to_inject, unsafe_allow_html=True)


account_create_page()

