import requests
import streamlit as st

from essentials import get_saldo, get_customer, get_account_info
from helpers import html_to_fstring


st.set_page_config(page_title="STRONG BANK - Deposit", initial_sidebar_state="collapsed", page_icon=FR"client\resources\images\logo_icon.png")

def deposit_page():
    with open('client/styles/style.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    with open('client/styles/deposit_page.html', 'r', encoding='utf8') as f:
        html = f.read()
        html_to_inject = html_to_fstring(html)
        st.markdown(html_to_inject, unsafe_allow_html=True)

    with st.form(key='deposit_form'):
        value = st.number_input(label='Valor:')
        description = st.text_input('Descrição:')
        submit = st.form_submit_button(label='Confirmar')

    html = """    <div style="display: flex; justify-content: center; align-items: center; margin: 20px;">
        <img src='data:image/png;base64,{img_to_bytes()}' style="width: 25%; height: auto;" class="img-fluid">
    </div>"""
    html_to_inject = html_to_fstring(html)
    st.markdown(html_to_inject, unsafe_allow_html=True)

    if value and submit:
        data = {'valor':float(value), 'descricao':description}
        response = requests.post(url='http://127.0.0.1:8000/depositar/', json=data, auth=get_account_info())

        if response.status_code == 200:
            st.legacy_caching.clear_cache()
            st.experimental_rerun()
        else:
            st.write(response.json())

    home_button_html = "<a target='_self' href='http://localhost:8501/home'><input type=button value='Voltar' class='botao_voltar'></a>"
    st.markdown(home_button_html, unsafe_allow_html=True)


deposit_page()

