import warnings
import streamlit as st

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

st.set_page_config(
    page_title="Orbitly",
    page_icon="🌌",
    layout="wide"
)

# Load CSS
from frontend.styles.load_css import load_css

load_css()

# Components
from frontend.components.hero import render_hero
from frontend.components.destination_strip import render_destination_strip
from frontend.components.trip_input import render_trip_input
from frontend.components.sidebar import render_sidebar
from frontend.utils.trip_manager import init_db

#create a table first in postgressql
init_db()

# Sidebar
trip_id = render_sidebar()



if not trip_id:
    st.info(
        "🌍 Create a trip from the sidebar to begin planning."
    )
    st.stop()

from main import app as travel_graph

config = {
    "configurable": {
        "thread_id": trip_id
    }
}

snapshot = travel_graph.get_state(config)

render_hero()
render_destination_strip()

if snapshot and snapshot.values:

    history = snapshot.values.get("messages", [])

    for msg in history:

        if msg.type == "human":
            with st.chat_message("user"):
                st.write(msg.content)

        elif msg.type == "ai":
            with st.chat_message("assistant"):
                st.write(msg.content)

user_query, generate = render_trip_input()

if generate and user_query:

    from frontend.components.pipeline import run_pipeline

    run_pipeline(
        user_query,
        trip_id
    )

    # st.rerun()