import streamlit as st


QUICK_PROMPTS = [
    {"emoji": "🏯", "label": "Japan under ₹2L"},
    {"emoji": "🗼", "label": "7days Luxury Paris Trip"},
    {"emoji": "🏝️", "label": "Bali Backpacking"},
    {"emoji": "🌃", "label": "Dubai Weekend"}
]


def render_trip_input():

    st.markdown(
        '<div class="input-title">✨ Describe Your Dream Trip</div>',
        unsafe_allow_html=True
    )

    # Initialize session state
    if "trip_query" not in st.session_state:
        st.session_state.trip_query = ""

    cols = st.columns(len(QUICK_PROMPTS))

    # Quick prompt buttons
    for col, prompt in zip(cols, QUICK_PROMPTS):

        with col:

            if st.button(
                f"{prompt['emoji']} {prompt['label']}",
                key=prompt['label'],
                use_container_width=True
            ):

                st.session_state.trip_query = prompt["label"]
                st.rerun()
                
    # Text area
    user_query = st.text_area(
        "Trip Description",
        value=st.session_state.trip_query,
        placeholder="✍️ Example: Plan a 7 days trip to Thailand from Mumbai under 50k budget.",
        height=140,
        label_visibility="collapsed"
    )

    # Keep updated value
    st.session_state.trip_query = user_query

    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        generate = st.button(
            "🚀 Launch Trip",
            use_container_width=True,
            type="primary"
        )

    if generate:
        query_to_process = user_query

        st.session_state.trip_query = ""

        return query_to_process, True

    return user_query, False    