import json
import streamlit as st
import requests
from essentials import get_account_info, get_customer

from helpers import html_to_fstring


st.set_page_config(page_title="STRONG BANK - Login", initial_sidebar_state="collapsed", page_icon=FR"client\resources\images\logo_icon.png")

def login_page():
    with open('client/styles/style.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

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
                "username": username,
                "password": password
                }
        with open('client/cookie.json', 'w') as f:
            json.dump(data, f)

        response = requests.post(url='http://127.0.0.1:8000/login/', json=data, auth=get_account_info())

        if response.status_code == 200:
            try:
                get_customer()
                st.markdown("<a target='_self' href='http://localhost:8501/home' class='botao_voltar' style='position:absolute; right:50px'><input type=button value='Avançar'></a>", unsafe_allow_html=True)
            except requests.JSONDecodeError:
                st.markdown("<a target='_self' href='http://localhost:8501/customer' class='botao_voltar' style='position:absolute; right:50px'><input type=button value='Avançar'></a>", unsafe_allow_html=True)

        else:
            st.write(response.json())

    html = """    <div style="display: flex; justify-content: center; align-items: center; margin: 20px;">
        <img src='data:image/png;base64,{img_to_bytes()}' style="width: 25%; height: auto;" class="img-fluid">
    </div>"""
    html_to_inject = html_to_fstring(html)

    st.markdown(html_to_inject, unsafe_allow_html=True)

    new_account_html = '<a target="_self" href="http://localhost:8501/register" style="color:#FFFFFF; font-weight:1000; padding:20px">Criar uma nova conta</a>'
    st.markdown(new_account_html, unsafe_allow_html=True)


login_page()

