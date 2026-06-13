import uuid
import streamlit as st

from streamlit_local_storage import LocalStorage

from frontend.utils.trip_manager import (
    create_trip,
    get_trips
)

local_storage = LocalStorage()


def get_user_id():

    user_id = local_storage.getItem("user_id")

    if not user_id:

        user_id = str(uuid.uuid4())

        local_storage.setItem(
            "user_id",
            user_id
        )

    return user_id


def render_sidebar():

    user_id = get_user_id()

    if "active_trip" not in st.session_state:
        st.session_state.active_trip = None

    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-logo-outer-div">
                <div class="sidebar-logo2">🌌</div>
                <div class="sidebar-logo">Orbitly</div>
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

                is_active = (
                    st.session_state.active_trip == trip_id
                )

                label = (
                    f"✅ {destination}"
                    if is_active
                    else f"🧳 {destination}"
                )

                if st.button(
                    label,
                    key=trip_id,
                    use_container_width=True
                ):

                    st.session_state.active_trip = trip_id

                    st.rerun()

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
            "✈️ Aviation Search"
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
            "✈️ Aviation AI",
            "🏨 StaySync AI",
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