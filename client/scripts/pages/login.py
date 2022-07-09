import json
import streamlit as st
import requests

from helpers import html_to_fstring


st.set_page_config(page_title="STRONG BANK", initial_sidebar_state="collapsed")

def login_page():
    with open('client/styles/style.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    with open('client/styles/login_page.html', 'r', encoding='utf8') as f:
        html = f.read()
        html_to_inject = html_to_fstring(html)
        st.markdown(html_to_inject, unsafe_allow_html=True)

    with st.form(key='login_form'):
        username = st.text_input(label='Usuário:')
        password = st.text_input(label='Senha:', type='password')
        submit = st.form_submit_button(label='Confirmar')

    if username and password and submit:
        data = {
                "conta_logada": username,
                "senha_logada": password
                }
        with open('client/cookie.json', 'w') as f:
            json.dump(data, f)

        st.markdown("<a target='_self' href='http://localhost:8501/home'><input type=button value='Avançar'></a>", unsafe_allow_html=True)
        # r = requests.post(url='http://127.0.0.1:8000/transferir/', json=data, auth=get_account_info())

    new_account_html = '<a target="_self" href="http://localhost:8501/criar_login" style="color:#000000; font-weight:1000; padding:20px">Criar uma nova conta</a>'
    st.markdown(new_account_html, unsafe_allow_html=True)


login_page()

