import streamlit as st
from frontend.constants import DESTINATIONS

def render_destination_strip():
    cols = st.columns(len(DESTINATIONS))
    for col, (name, img_url) in zip(cols, DESTINATIONS):
        with col:
            st.markdown(f"""
            <div class="destination-card">
                <img src="{img_url}" class="destination-img" />
                <div class="destination-overlay">{name}</div>
            </div>
            """, unsafe_allow_html=True)