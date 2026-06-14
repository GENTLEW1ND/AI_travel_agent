# import warnings
# import streamlit as st

# warnings.filterwarnings("ignore")
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# st.set_page_config(
#     page_title="Orbitly",
#     page_icon="🌌",
#     layout="wide"
# )

# print("1. App starting") #debug

# # Load CSS
# from frontend.styles.load_css import load_css

# load_css()

# # Components
# from frontend.components.hero import render_hero
# from frontend.components.destination_strip import render_destination_strip
# from frontend.components.trip_input import render_trip_input
# from frontend.components.sidebar import render_sidebar
# from frontend.utils.trip_manager import init_db
# from frontend.utils.graph_manager import get_graph

# print("2. Imported init_db") #debug

# #create a table first in postgressql
# init_db()

# print("3. init_db completed") # debug

# # Sidebar
# trip_id = render_sidebar()

# print("4. Sidebar rendered") #debug

# if not trip_id:
#     st.info(
#         "🌍 Create a trip from the sidebar to begin planning."
#     )
#     st.stop()
    


# travel_graph = get_graph()


# config = {
#     "configurable": {
#         "thread_id": trip_id
#     }
# }


# try:
#     snapshot = travel_graph.get_state(config)
# except Exception as e:
#     print(f"State retrieval failed: {e}")
#     snapshot = None


# render_hero()
# render_destination_strip()

# if snapshot and snapshot.values:

#     history = snapshot.values.get("messages", [])

#     for msg in history:

#         if msg.type == "human":
#             with st.chat_message("user"):
#                 st.write(msg.content)

#         elif msg.type == "ai":
#             with st.chat_message("assistant"):
#                 st.write(msg.content)

# user_query, generate = render_trip_input()

# print("6. get_state completed") #debug

# if generate and user_query:

#     from frontend.components.pipeline import run_pipeline

#     run_pipeline(
#         user_query,
#         trip_id
#     )

#     # st.rerun()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# import warnings
# import streamlit as st

# warnings.filterwarnings("ignore")
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# st.set_page_config(
#     page_title="Orbitly",
#     page_icon="🌌",
#     layout="wide"
# )

# # Load CSS
# from frontend.styles.load_css import load_css
# load_css()

# # Components
# from frontend.components.hero import render_hero
# from frontend.components.destination_strip import render_destination_strip
# from frontend.components.trip_input import render_trip_input
# from frontend.components.sidebar import render_sidebar
# from frontend.utils.trip_manager import init_db
# from frontend.utils.graph_manager import get_graph

# # Init DB
# init_db()

# # Sidebar — returns trip_id, user_id is in st.session_state["user_id"]
# trip_id = render_sidebar()
# print(f"DEBUG [app] user_id={st.session_state.get('user_id')} trip_id={trip_id}")


# # user_id is set inside render_sidebar via get_user_id()
# user_id = st.session_state.get("user_id")

# print(f"DEBUG app.py — user_id: {user_id}, trip_id: {trip_id}")

# if not trip_id:
#     render_hero()
#     render_destination_strip()
#     st.info("🌍 Create a trip from the sidebar to begin planning.")
#     st.stop()

# # Scope thread_id to user + trip so each browser has isolated history
# thread_id = f"{user_id}::{trip_id}"

# print(f"DEBUG app.py — thread_id: {thread_id}")

# travel_graph = get_graph()

# config = {
#     "configurable": {
#         "thread_id": thread_id
#     }
# }

# # Load chat history for this user's trip from Postgres checkpointer
# try:
#     snapshot = travel_graph.get_state(config)
# except Exception as e:
#     print(f"State retrieval failed: {e}")
#     snapshot = None

# render_hero()
# render_destination_strip()

# if snapshot and snapshot.values:

#     history = snapshot.values.get("messages", [])

#     for msg in history:

#         if msg.type == "human":
#             with st.chat_message("user"):
#                 st.write(msg.content)

#         elif msg.type == "ai":
#             # Skip internal agent messages
#             if msg.content in (
#                 "Flight information fetched",
#                 "Hotel information fetched"
#             ):
#                 continue
#             with st.chat_message("assistant"):
#                 st.write(msg.content)

# user_query, generate = render_trip_input()

# if generate and user_query:

#     from frontend.components.pipeline import run_pipeline

#     run_pipeline(
#         user_query,
#         trip_id,
#         user_id
#     )

#     # st.rerun()




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# import warnings
# import streamlit as st

# warnings.filterwarnings("ignore")
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# st.set_page_config(
#     page_title="Orbitly",
#     page_icon="🌌",
#     layout="wide"
# )

# # Load CSS
# from frontend.styles.load_css import load_css
# load_css()

# # Components
# from frontend.components.hero import render_hero
# from frontend.components.destination_strip import render_destination_strip
# from frontend.components.trip_input import render_trip_input
# from frontend.components.sidebar import render_sidebar, render_login, get_user_id
# from frontend.utils.trip_manager import init_db
# from frontend.utils.graph_manager import get_graph

# # Init DB
# init_db()

# # ── Login Gate ──────────────────────────────────────────────────────────
# # If not logged in, show the login screen and stop here
# if not get_user_id():
#     render_login()
#     st.stop()
# # ─────────────────────────────────────────────────────────────────────────

# # Sidebar — returns active trip_id (or None)
# trip_id = render_sidebar()

# user_id = st.session_state.get("user_id")

# if not trip_id:
#     render_hero()
#     render_destination_strip()
#     st.info("🌍 Create a trip from the sidebar to begin planning.")
#     st.stop()

# # Scope thread_id to user + trip so each user has isolated history
# thread_id = f"{user_id}::{trip_id}"

# travel_graph = get_graph()

# config = {
#     "configurable": {
#         "thread_id": thread_id
#     }
# }

# # Load chat history for this user's trip
# try:
#     snapshot = travel_graph.get_state(config)
# except Exception as e:
#     print(f"State retrieval failed: {e}")
#     snapshot = None

# render_hero()
# render_destination_strip()

# if snapshot and snapshot.values:

#     history = snapshot.values.get("messages", [])

#     for msg in history:

#         if msg.type == "human":
#             with st.chat_message("user"):
#                 st.write(msg.content)

#         elif msg.type == "ai":
#             if msg.content in (
#                 "Flight information fetched",
#                 "Hotel information fetched"
#             ):
#                 continue
#             with st.chat_message("assistant"):
#                 st.write(msg.content)

# user_query, generate = render_trip_input()

# if generate and user_query:

#     from frontend.components.pipeline import run_pipeline

#     run_pipeline(
#         user_query,
#         trip_id,
#         user_id
#     )

#     st.rerun()



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
from frontend.components.sidebar import render_sidebar, render_login, get_user_id
from frontend.utils.trip_manager import init_db
from frontend.utils.graph_manager import get_graph

# Init DB
init_db()

# ── Login Gate ──────────────────────────────────────────────────────────
# If not logged in, show the login screen and stop here
if not get_user_id():
    render_login()
    st.stop()
# ─────────────────────────────────────────────────────────────────────────

# Sidebar — returns active trip_id (or None)
trip_id = render_sidebar()

user_id = st.session_state.get("user_id")

if not trip_id:
    render_hero()
    render_destination_strip()
    st.info("🌍 Create a trip from the sidebar to begin planning.")
    st.stop()

# Scope thread_id to user + trip so each user has isolated history
thread_id = f"{user_id}::{trip_id}"

travel_graph = get_graph()

config = {
    "configurable": {
        "thread_id": thread_id
    }
}

# Load chat history for this user's trip
try:
    snapshot = travel_graph.get_state(config)
except Exception as e:
    print(f"State retrieval failed: {e}")
    snapshot = None

render_hero()
render_destination_strip()

if snapshot and snapshot.values:

    history = snapshot.values.get("messages", [])

    for msg in history:

        if msg.type == "human":
            with st.chat_message("user"):
                st.write(msg.content)

        elif msg.type == "ai":
            if msg.content in (
                "Flight information fetched",
                "Hotel information fetched"
            ):
                continue
            with st.chat_message("assistant"):
                st.write(msg.content)

user_query, generate = render_trip_input()




if generate and user_query:

    from frontend.utils.intent_classifier import classify_intent

    intent = classify_intent(user_query)

    if intent == "NON_TRAVEL":

        st.chat_message("assistant").write(
            """
I'm Orbitly 🌌

I help with:

✈️ Flight planning
🏨 Hotel recommendations
🗺️ Travel itineraries
🌍 Destination suggestions
💰 Budget travel plans

Please ask a travel-related question.
"""
        )

    else:

        from frontend.components.pipeline import run_pipeline

        run_pipeline(
            user_query,
            trip_id,
            user_id
        )

  