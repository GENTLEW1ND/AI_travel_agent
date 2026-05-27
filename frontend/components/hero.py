import streamlit as st

def render_hero():
    # Logo
    st.markdown("""
    <div class="orbitly-logo-wrapper">
        <div class="orbit-ring orbit-ring-1"></div>
        <div class="orbit-ring orbit-ring-2"></div>
        <div class="orbit-core">🌌</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero
    st.markdown("""
    <div class="hero-wrapper">
        <div class="glow glow-1"></div>
        <div class="glow glow-2"></div>
        <div class="hero-content">
            <div class="hero-badge">✦ MULTI AGENT AI SYSTEM</div>
            <div class="hero-title">Orbitly</div>
            <div class="hero-sub">
                Build extraordinary trips with autonomous AI travel agents.
                Flights, stays, itineraries, and smart planning — all orchestrated in real time.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)