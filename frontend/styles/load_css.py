import streamlit as st
from pathlib import Path

def load_css():
    css_file = Path(__file__).parent / "main.css"
    with open(css_file, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)