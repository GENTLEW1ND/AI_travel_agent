import streamlit as st

from langchain_core.messages import HumanMessage

from frontend.constants import AGENT_META
from frontend.utils.save_plan import save_travel_plan

from frontend.utils.graph_manager import get_graph


def run_pipeline(user_query, thread_id):
    """Execute the multi-agent travel planning pipeline."""
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    
    collected = {
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "final_response": "",
        "llm_calls": 0
    }
    
    st.markdown(
        "<div class='section-title'>🤖 Orbit AI Pipeline</div>",
        unsafe_allow_html=True
    )
    
    # Add a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        travel_graph = get_graph()
        for i, chunk in enumerate(travel_graph.stream(
            {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0,
            },
            config=config,
            stream_mode="updates",
        )):
            # Update progress
            progress = (i + 1) / 4  # Assuming 4 agents
            progress_bar.progress(min(progress, 1.0))
            
            for node_name, state_update in chunk.items():
                icon, label = AGENT_META.get(node_name, ("🔧", node_name))
                status_text.text(f"{icon} {label} processing...")
                
                with st.status(f"{icon} {label}", expanded=True, state="complete"):
                    if node_name == "flight_agent":
                        text = state_update.get("flight_results", "Couldn't find any relevant flight for the provided route.")
                        collected["flight_results"] = text
                        st.markdown(text)
                    
                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text)
                    
                    if node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text)
                    
                    elif node_name == "final_agent":
                        msgs = state_update.get("messages", [])
                        text = msgs[-1].content if msgs else ""
                        collected["final_response"] = text
                        st.markdown(text)
                
                collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"Pipeline error: {str(e)}")
        return
    
    # Display metrics
    st.markdown(
        f"""
        <div class='metric-wrapper'>
            <div class='metric-card'>
                <div class='metric-value'>4</div>
                <div class='metric-label'>AI Agents</div>
            </div>
            <div class='metric-card'>
                <div class='metric-value'>{collected['llm_calls']}</div>
                <div class='metric-label'>LLM Calls</div>
            </div>
            <div class='metric-card'>
                <div class='metric-value'>✅</div>
                <div class='metric-label'>Completed</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display final response
    st.markdown(
        f"""
        <div class='final-card'>
            {collected['final_response']}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    
    try:
        filename, file_content = save_travel_plan(
            user_query,
            thread_id,
            collected
        )

        # st.success("save_plan completed")

    except Exception as e:
            st.error(f"save_plan failed: {e}")
            raise
    
    st.download_button(
        "⬇️ Download Journey",
        data=file_content,
        file_name=filename,
        mime="text/markdown",
        use_container_width=True
    )