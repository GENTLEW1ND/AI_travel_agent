import random
import streamlit as st

from streamlit_cookies_manager import EncryptedCookieManager


cookies = EncryptedCookieManager(
    prefix="orbitly_",
    password="orbitly_secret_key"
)

if not cookies.ready():
    st.stop()


def generate_session_id():

    names = [
        "orbit",
        "nova",
        "astro",
        "vega",
        "luna",
        "cosmo"
    ]

    return f"{random.choice(names)}-{random.randint(1000,9999)}"


def render_sidebar():

    if "thread_id" not in cookies:

        cookies["thread_id"] = generate_session_id()

        cookies.save()

    thread_id = cookies["thread_id"]

    with st.sidebar:

        st.markdown(
            "<div class='sidebar-logo'>🌌 Orbitly</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='sidebar-sub'>AI Travel Command Center</div>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown(
            f"""
            <div class="session-card">
                <div class="session-label">🛰️ Persistent Travel Identity</div>
                <div class="session-id">{thread_id}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='side-title'>⚡ Powered By</div>",
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
                f"<div class='side-chip'>{tech}</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "<div class='side-title'>🤖 AI Agent Pipeline</div>",
            unsafe_allow_html=True
        )

        agents = [
            "✈️ Flight Agent",
            "🏩 Hotel Agent",
            "🗺 Itinerary Agent",
            "🧠 Orbit Core"
        ]

        for agent in agents:

            st.markdown(
                f"<div class='side-chip'>{agent}</div>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class='orbit-footer'>
                Built for next-gen autonomous travel experiences ✨
            </div>
            """,
            unsafe_allow_html=True
        )

    return thread_id