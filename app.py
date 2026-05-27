import streamlit as st

st.set_page_config(page_title="Orbitly", page_icon="🌌", layout="wide")

# Load CSS
from frontend.styles.load_css import load_css
load_css()

# Import and render
from frontend.components.hero import render_hero
from frontend.components.destination_strip import render_destination_strip
from frontend.components.trip_input import render_trip_input
from frontend.components.sidebar import render_sidebar

thread_id = render_sidebar()
render_hero()
render_destination_strip()
user_query, generate = render_trip_input()

if generate and user_query:
    from frontend.components.pipeline import run_pipeline
    run_pipeline(user_query, thread_id)