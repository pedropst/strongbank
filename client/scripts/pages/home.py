import streamlit as st

from essentials import get_saldo, get_cliente
from helpers import html_to_fstring


st.set_page_config(page_title="STRONG BANK", initial_sidebar_state="collapsed")

def home_page():
    with open('client/styles/home_page.html', 'r', encoding='utf8') as f:
        html = f.read()
        html_to_inject = html_to_fstring(html)
        st.markdown(html_to_inject, unsafe_allow_html=True)


home_page()

