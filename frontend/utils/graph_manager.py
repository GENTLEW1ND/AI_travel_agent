import streamlit as st
from main import create_app

@st.cache_resource
def get_graph():
    return create_app()