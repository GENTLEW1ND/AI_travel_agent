import re
import hashlib
import streamlit as st

from frontend.utils.trip_manager import (
    create_trip,
    get_trips,
    get_or_create_user
)

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def email_to_user_id(email: str) -> str:
    """
    Deterministic id from email — same email always
    produces the same user_id.
    """
    return hashlib.sha256(
        email.strip().lower().encode()
    ).hexdigest()[:32]


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip()))


def render_login():
    """
    Renders a simple email-based login screen.
    Validates email format before proceeding.
    """

    st.markdown(
        """
        <div class="orbitly-logo-wrapper">
            <div class="orbit-ring orbit-ring-1"></div>
            <div class="orbit-ring orbit-ring-2"></div>
            <div class="orbit-core">🌌</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-content" style="text-align:center; margin-bottom: 2rem;">
            <div class="hero-title" style="font-size: 3rem;">Welcome to Orbitly</div>
            <div class="hero-sub">
                Enter your email to access your trips. Your trips will
                always be waiting for you — on any device.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        email = st.text_input(
            "Email",
            placeholder="e.g. raj@example.com",
            label_visibility="collapsed"
        )

        if st.button(
            "🚀 Continue",
            use_container_width=True,
            type="primary"
        ):
            email_clean = email.strip()

            if not email_clean:
                st.warning("Please enter your email to continue.")

            elif not is_valid_email(email_clean):
                st.error("Please enter a valid email address.")

            else:
                user_id = email_to_user_id(email_clean)

                # Use the part before @ as a friendly display name
                display_name = email_clean.split("@")[0]

                get_or_create_user(
                    user_id,
                    display_name=display_name,
                    email=email_clean.lower()
                )

                st.session_state["user_id"] = user_id
                st.session_state["display_name"] = display_name
                st.session_state["email"] = email_clean.lower()

                st.rerun()


def get_user_id():
    """
    Returns user_id if logged in, else None.
    """
    return st.session_state.get("user_id")


def render_sidebar():

    user_id = get_user_id()

    if not user_id:
        return None

    display_name = st.session_state.get("display_name", "Traveler")
    email = st.session_state.get("email", "")

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
                    👤 Signed in as
                </div>
                <div class="session-id">
                    {email}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🚪 Sign out", use_container_width=True):
            st.session_state.pop("user_id", None)
            st.session_state.pop("display_name", None)
            st.session_state.pop("email", None)
            st.session_state.pop("active_trip", None)
            st.rerun()

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

        for tech in [
            "🔗 LangGraph",
            "🧠 Groq · LLaMA 3.3",
            "🐘 PostgreSQL",
            "🔍 Tavily Search",
            "✈️ Aviation Search"
        ]:
            st.markdown(
                f'<div class="side-chip">{tech}</div>',
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

        for agent in [
            "✈️ Aviation AI",
            "🏨 StaySync AI",
            "🗺 RouteMind AI",
            "🧠 Orbit Core"
        ]:
            st.markdown(
                f'<div class="side-chip">{agent}</div>',
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