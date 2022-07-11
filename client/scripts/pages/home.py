from re import A
from tkinter import Image
import streamlit as st

from essentials import get_saldo, get_cliente
from helpers import html_to_fstring


st.set_page_config(page_title="STRONG BANK - Home", initial_sidebar_state="collapsed")

def home_page_novo():
    with open('client/styles/style.css', 'r') as f:
        css_to_inject = f.read()
        st.markdown(f'<style>{css_to_inject}</style>', unsafe_allow_html=True)

    with st.container():
        with open('client/styles/home_page.html', 'r', encoding='utf8') as f:
            html = f.read()
            html_to_inject = html_to_fstring(html)
            st.markdown(html_to_inject, unsafe_allow_html=True)

    home_button_html = "<a target='_self' href='http://localhost:8501/login'><input type=button value='Voltar' class='botao_voltar'></a>"
    st.markdown(home_button_html, unsafe_allow_html=True)


# st.image(RF"client\resources\images\logo.png")
home_page_novo()



