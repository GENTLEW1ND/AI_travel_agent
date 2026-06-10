import random
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from frontend.utils.trip_manager import (
    create_trip,
    get_trips
)


def generate_user_id():

    names = [
        "orbit",
        "nova",
        "astro",
        "vega",
        "luna",
        "cosmo"
    ]

    return f"{random.choice(names)}-{random.randint(1000,9999)}"



cookies = EncryptedCookieManager(
    prefix="orbitly_",
    password="orbitly_secret_key"
)
if not cookies.ready():
    st.stop()

def render_sidebar():


    if "user_id" not in cookies:

        cookies["user_id"] = generate_user_id()

        cookies.save()

    user_id = cookies["user_id"]

    if "active_trip" not in st.session_state:
        st.session_state.active_trip = None

   
    with st.sidebar:

        # Logo
        st.markdown(
            """
            <div class="sidebar-logo">
                🌌 Orbitly
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="sidebar-sub">
                AI Travel Command Center
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Current User
        st.markdown(
            f"""
            <div class="session-card">
                <div class="session-label">
                    👤 User
                </div>
                <div class="session-id">
                    {user_id}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Create Trip
        st.markdown(
            """
            <div class="side-title">
                🌍 My Trips
            </div>
            """,
            unsafe_allow_html=True
        )

        destination = st.text_input(
            "Destination",
            placeholder="Japan, Singapore, Bali..."
        )

        if st.button(
            "➕ Create New Trip",
            use_container_width=True
        ):

            if destination.strip():

                trip_id = create_trip(
                    user_id,
                    destination
                )

                st.session_state.active_trip = trip_id

                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Load Trips from PostgreSQL
        trips = get_trips(user_id)

        if trips:

            st.markdown(
                """
                <div class="side-title">
                    📂 Existing Trips
                </div>
                """,
                unsafe_allow_html=True
            )

            for trip_id, destination in trips:

                if st.button(
                    f"🧳 {destination}",
                    key=trip_id,
                    use_container_width=True
                ):
                    st.session_state.active_trip = trip_id
                    st.rerun()

        # Active Trip Card
        if st.session_state.active_trip:

            st.markdown(
                f"""
                <div class="session-card">

                    <div class="session-label">
                        🚀 Active Trip
                    </div>
                    <div class="session-id">
                        {st.session_state.active_trip}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Tech Stack
        st.markdown(
            """
            <div class="side-title">
                ⚡ Powered By
            </div>
            """,
            unsafe_allow_html=True
        )

        tech_stack = [
            "🔗 LangGraph",
            "🧠 Groq · LLaMA 3.3",
            "🐘 PostgreSQL",
            "🔍 Tavily Search",
            "🌦 Weather Intelligence"
        ]

        for tech in tech_stack:

            st.markdown(
                f"""
                <div class="side-chip">
                    {tech}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            """
            <div class="side-title">
                🤖 AI Agent Pipeline
            </div>
            """,
            unsafe_allow_html=True
        )

        agents = [
            "🌦 ClimateMind AI",
            "🏨 StaySync AI",
            "🍜 LocalLens AI",
            "🗺 RouteMind AI",
            "🧠 Orbit Core"
        ]

        for agent in agents:

            st.markdown(
                f"""
                <div class="side-chip">
                    {agent}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="orbit-footer">
                Built for next-gen autonomous travel experiences ✨
            </div>
            """,
            unsafe_allow_html=True
        )

    return st.session_state.active_trip