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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import uuid
# import streamlit as st
# from streamlit_cookies_controller import CookieController

# from frontend.utils.trip_manager import (
#     create_trip,
#     get_trips
# )


# def get_cookie_controller():
#     return CookieController()


# def get_user_id():
#     """
#     Resolution order:
#     1. session_state  — fastest, avoids all I/O
#     2. cookie         — persists across browser restarts
#     3. query param    — fallback if cookie not readable yet
#     4. generate new   — first ever visit
#     """

#     if st.session_state.get("user_id"):
#         print(f"DEBUG [session]: {st.session_state['user_id']}")
#         return st.session_state["user_id"]

#     controller = get_cookie_controller()

#     try:
#         cookie_id = controller.get("orbitly_uid")
#     except Exception as e:
#         print(f"DEBUG [cookie error]: {e}")
#         cookie_id = None

#     print(f"DEBUG [cookie value]: {cookie_id}")
#     print(f"DEBUG [query param]: {st.query_params.get('uid', 'NONE')}")

#     if cookie_id and isinstance(cookie_id, str) and cookie_id.strip():
#         user_id = cookie_id.strip()
#         st.session_state["user_id"] = user_id
#         # Also write to query param so it survives a refresh
#         # before cookie is readable again
#         st.query_params["uid"] = user_id
#         return user_id

#     # 3. Cookie not ready yet — check query param as fallback
#     # query param is set by us on previous render, not user-facing
#     uid_from_param = st.query_params.get("uid", "").strip()

#     if uid_from_param:
#         user_id = uid_from_param
#         st.session_state["user_id"] = user_id
#         # Try to write cookie again now that controller may be ready
#         try:
#             controller.set(
#                 "orbitly_uid",
#                 user_id,
#                 max_age=30 * 24 * 60 * 60
#             )
#         except Exception:
#             pass
#         print(f"DEBUG [from query param]: {user_id}")
#         return user_id

#     # 4. Truly first visit — generate uuid
#     user_id = str(uuid.uuid4())
#     print(f"DEBUG [generated]: {user_id}")

#     # Write to query param immediately (works on this render)
#     st.query_params["uid"] = user_id

#     # Write to cookie (may need one rerun to be readable)
#     try:
#         controller.set(
#             "orbitly_uid",
#             user_id,
#             max_age=30 * 24 * 60 * 60
#         )
#     except Exception:
#         pass

#     st.session_state["user_id"] = user_id
#     return user_id


# def render_sidebar():

#     user_id = get_user_id()

#     if not user_id:
#         st.stop()

#     st.session_state["user_id"] = user_id

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
#                     {user_id[:8]}...{user_id[-4:]}
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

#         for tech in [
#             "🔗 LangGraph",
#             "🧠 Groq · LLaMA 3.3",
#             "🐘 PostgreSQL",
#             "🔍 Tavily Search",
#             "✈️ Aviation Search"
#         ]:
#             st.markdown(
#                 f'<div class="side-chip">{tech}</div>',
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

#         for agent in [
#             "✈️ Aviation AI",
#             "🏨 StaySync AI",
#             "🗺 RouteMind AI",
#             "🧠 Orbit Core"
#         ]:
#             st.markdown(
#                 f'<div class="side-chip">{agent}</div>',
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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# import hashlib
# import streamlit as st

# from frontend.utils.trip_manager import (
#     create_trip,
#     get_trips,
#     get_or_create_user
# )


# def name_to_user_id(name: str) -> str:
#     """
#     Deterministic uuid-like id from a name.
#     Same name always produces the same id — no passwords needed.
#     """
#     return hashlib.sha256(
#         name.strip().lower().encode()
#     ).hexdigest()[:32]


# def render_login():
#     """
#     Renders a simple name-based login screen.
#     Returns True once the user is logged in.
#     """

#     st.markdown(
#         """
#         <div class="orbitly-logo-wrapper">
#             <div class="orbit-ring orbit-ring-1"></div>
#             <div class="orbit-ring orbit-ring-2"></div>
#             <div class="orbit-core">🌌</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     st.markdown(
#         """
#         <div class="hero-content" style="text-align:center; margin-bottom: 2rem;">
#             <div class="hero-title" style="font-size: 3rem;">Welcome to Orbitly</div>
#             <div class="hero-sub">
#                 Enter your name to access your trips. Same name, your trips
#                 will always be waiting for you — on any device.
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     col1, col2, col3 = st.columns([1, 2, 1])

#     with col2:

#         name = st.text_input(
#             "Your Name",
#             placeholder="e.g. Raj Chauhan",
#             label_visibility="collapsed"
#         )

#         if st.button(
#             "🚀 Continue",
#             use_container_width=True,
#             type="primary"
#         ):
#             if name.strip():

#                 user_id = name_to_user_id(name)
#                 get_or_create_user(user_id, display_name=name.strip())

#                 st.session_state["user_id"] = user_id
#                 st.session_state["display_name"] = name.strip()

#                 st.rerun()
#             else:
#                 st.warning("Please enter your name to continue.")

#     return False


# def get_user_id():
#     """
#     Returns user_id if logged in, else None.
#     Login state lives in session_state for this session only.
#     """
#     return st.session_state.get("user_id")


# def render_sidebar():

#     user_id = get_user_id()

#     if not user_id:
#         # Not logged in — caller (app.py) should show login screen
#         return None

#     display_name = st.session_state.get("display_name", "Traveler")

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
#                     👤 Welcome back
#                 </div>
#                 <div class="session-id">
#                     {display_name}
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         if st.button("🚪 Switch User", use_container_width=True):
#             st.session_state.pop("user_id", None)
#             st.session_state.pop("display_name", None)
#             st.session_state.pop("active_trip", None)
#             st.rerun()

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

#         for tech in [
#             "🔗 LangGraph",
#             "🧠 Groq · LLaMA 3.3",
#             "🐘 PostgreSQL",
#             "🔍 Tavily Search",
#             "✈️ Aviation Search"
#         ]:
#             st.markdown(
#                 f'<div class="side-chip">{tech}</div>',
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

#         for agent in [
#             "✈️ Aviation AI",
#             "🏨 StaySync AI",
#             "🗺 RouteMind AI",
#             "🧠 Orbit Core"
#         ]:
#             st.markdown(
#                 f'<div class="side-chip">{agent}</div>',
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



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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