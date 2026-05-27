# test_setup.py
import streamlit as st

st.set_page_config(page_title="Orbitly Test", layout="wide")

# Test 1: Basic HTML rendering
st.markdown("## Test 1: Basic HTML")
st.markdown('<div style="background: blue; padding: 20px; color: white;">Basic HTML works!</div>', unsafe_allow_html=True)

# Test 2: CSS loading
st.markdown("## Test 2: CSS Loading")
with open("frontend/assets/style.css") as f:
    css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.success("CSS loaded successfully!")

# Test 3: Hero rendering
st.markdown("## Test 3: Hero Component")
from frontend.components.hero import render_hero
render_hero()

# Test 4: Logo rendering
st.markdown("## Test 4: Logo Component")
from frontend.components.logo import render_logo
render_logo()