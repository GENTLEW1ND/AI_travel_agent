import streamlit as st


def render_logo():

    st.markdown(
        """
        <div class="orbitly-logo-wrapper">

            <div class="orbit-ring orbit-ring-1"></div>

            <div class="orbit-ring orbit-ring-2"></div>

            <div class="orbit-core">
                🌌
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )