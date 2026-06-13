# import uuid
# import streamlit as st

# from streamlit_local_storage import LocalStorage

# from frontend.utils.trip_manager import (
#     create_trip,
#     get_trips
# )

# local_storage = LocalStorage()


# def get_user_id():

#     user_id = local_storage.getItem("user_id")

#     if not user_id:

#         user_id = str(uuid.uuid4())

#         local_storage.setItem(
#             "user_id",
#             user_id
#         )

#     return user_id


# def render_sidebar():

#     user_id = get_user_id()

#     if "active_trip" not in st.session_state:
#         st.session_state.active_trip = None

#     with st.sidebar:

#         st.markdown(
#             """
#             <div class="sidebar-logo-outer-div">
#                 <div class="sidebar-logo2">🌌</div>
#                 <div class="sidebar-logo">Orbitly</div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         st.markdown(
#             """
#             <div class="sidebar-sub">
#                 AI Travel Command Center
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         st.markdown("---")

#         st.markdown(
#             f"""
#             <div class="session-card">
#                 <div class="session-label">
#                     👤 User
#                 </div>
#                 <div class="session-id">
#                     {user_id}
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         st.markdown("<br>", unsafe_allow_html=True)

#         st.markdown(
#             """
#             <div class="side-title">
#                 🌍 My Trips
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         destination = st.text_input(
#             "Destination",
#             placeholder="Japan, Singapore, Bali..."
#         )

#         if st.button(
#             "➕ Create New Trip",
#             use_container_width=True
#         ):

#             if destination.strip():

#                 trip_id = create_trip(
#                     user_id,
#                     destination
#                 )

#                 st.session_state.active_trip = trip_id

#                 st.rerun()

#         st.markdown("<br>", unsafe_allow_html=True)

#         trips = get_trips(user_id)

#         if trips:

#             st.markdown(
#                 """
#                 <div class="side-title">
#                     📂 Existing Trips
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             for trip_id, destination in trips:

#                 is_active = (
#                     st.session_state.active_trip == trip_id
#                 )

#                 label = (
#                     f"✅ {destination}"
#                     if is_active
#                     else f"🧳 {destination}"
#                 )

#                 if st.button(
#                     label,
#                     key=trip_id,
#                     use_container_width=True
#                 ):

#                     st.session_state.active_trip = trip_id

#                     st.rerun()

#         if st.session_state.active_trip:

#             st.markdown(
#                 f"""
#                 <div class="session-card">
#                     <div class="session-label">
#                         🚀 Active Trip
#                     </div>
#                     <div class="session-id">
#                         {st.session_state.active_trip}
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#         st.markdown("---")

#         st.markdown(
#             """
#             <div class="side-title">
#                 ⚡ Powered By
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         tech_stack = [
#             "🔗 LangGraph",
#             "🧠 Groq · LLaMA 3.3",
#             "🐘 PostgreSQL",
#             "🔍 Tavily Search",
#             "✈️ Aviation Search"
#         ]

#         for tech in tech_stack:

#             st.markdown(
#                 f"""
#                 <div class="side-chip">
#                     {tech}
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#         st.markdown(
#             """
#             <div class="side-title">
#                 🤖 AI Agent Pipeline
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         agents = [
#             "✈️ Aviation AI",
#             "🏨 StaySync AI",
#             "🗺 RouteMind AI",
#             "🧠 Orbit Core"
#         ]

#         for agent in agents:

#             st.markdown(
#                 f"""
#                 <div class="side-chip">
#                     {agent}
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#         st.markdown("<br>", unsafe_allow_html=True)

#         st.markdown(
#             """
#             <div class="orbit-footer">
#                 Built for next-gen autonomous travel experiences ✨
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#     return st.session_state.active_trip


import uuid
import streamlit as st
from streamlit_cookies_controller import CookieController

from frontend.utils.trip_manager import (
    create_trip,
    get_trips
)


def get_cookie_controller():
    return CookieController()


def get_user_id():
    """
    Resolution order:
    1. session_state  — fastest, avoids all I/O
    2. cookie         — persists across browser restarts
    3. query param    — fallback if cookie not readable yet
    4. generate new   — first ever visit
    """

    if st.session_state.get("user_id"):
        print(f"DEBUG [session]: {st.session_state['user_id']}")
        return st.session_state["user_id"]

    controller = get_cookie_controller()

    try:
        cookie_id = controller.get("orbitly_uid")
    except Exception as e:
        print(f"DEBUG [cookie error]: {e}")
        cookie_id = None

    print(f"DEBUG [cookie value]: {cookie_id}")
    print(f"DEBUG [query param]: {st.query_params.get('uid', 'NONE')}")

    if cookie_id and isinstance(cookie_id, str) and cookie_id.strip():
        user_id = cookie_id.strip()
        st.session_state["user_id"] = user_id
        # Also write to query param so it survives a refresh
        # before cookie is readable again
        st.query_params["uid"] = user_id
        return user_id

    # 3. Cookie not ready yet — check query param as fallback
    # query param is set by us on previous render, not user-facing
    uid_from_param = st.query_params.get("uid", "").strip()

    if uid_from_param:
        user_id = uid_from_param
        st.session_state["user_id"] = user_id
        # Try to write cookie again now that controller may be ready
        try:
            controller.set(
                "orbitly_uid",
                user_id,
                max_age=30 * 24 * 60 * 60
            )
        except Exception:
            pass
        print(f"DEBUG [from query param]: {user_id}")
        return user_id

    # 4. Truly first visit — generate uuid
    user_id = str(uuid.uuid4())
    print(f"DEBUG [generated]: {user_id}")

    # Write to query param immediately (works on this render)
    st.query_params["uid"] = user_id

    # Write to cookie (may need one rerun to be readable)
    try:
        controller.set(
            "orbitly_uid",
            user_id,
            max_age=30 * 24 * 60 * 60
        )
    except Exception:
        pass

    st.session_state["user_id"] = user_id
    return user_id


def render_sidebar():

    user_id = get_user_id()

    if not user_id:
        st.stop()

    st.session_state["user_id"] = user_id

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
                    {user_id[:8]}...{user_id[-4:]}
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