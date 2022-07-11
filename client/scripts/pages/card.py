import requests
import streamlit as st
from traitlets import default

from essentials import get_saldo, get_cliente, get_cartao, get_account_info
from helpers import html_to_fstring_com_iterador, html_to_fstring


st.set_page_config(page_title="STRONG BANK - Cartões", initial_sidebar_state="collapsed")

def card_page():
    n = 0

    with open('client/styles/style.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    with open('client/styles/card_3d.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    for n in range(len(get_cartao())):
        with open('client/styles/card.html', 'r', encoding='utf8') as f:
            html = f.read()
            html_to_inject = html_to_fstring_com_iterador(html, n)
            st.markdown(html_to_inject, unsafe_allow_html=True)
   
    a, b, c, d, e = st.columns(5)
    with b:
        bloquear = st.select_slider('Bloqueado', options=['SIM', 'NÃO'], value='NÃO')

        if bloquear == 'SIM':
            print('BLOQUEADO')
            #REQUEST PARA BLOQUEAR O CARTAO
            # st.legacy_caching.clear_cache()
            # st.experimental_rerun()

    with d:
        fatura = st.selectbox('Fatura', options=['07/22', '08/22', '09/22'])

    html = """    <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
        <img src='data:image/png;base64,{img_to_bytes()}' style="width: 25%; height: auto;" class="img-fluid">
    </div>"""
    html_to_inject = html_to_fstring(html)

    st.markdown(html_to_inject, unsafe_allow_html=True)

    home_button_html = "<a target='_self' href='http://localhost:8501/home'><input type=button value='Voltar' class='botao_voltar'></a>"
    st.markdown(home_button_html, unsafe_allow_html=True)


card_page()

