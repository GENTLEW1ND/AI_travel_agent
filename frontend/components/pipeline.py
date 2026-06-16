# import streamlit as st

# from langchain_core.messages import HumanMessage

# from frontend.constants import AGENT_META
# from frontend.utils.save_plan import save_travel_plan

# from frontend.utils.graph_manager import get_graph


# def run_pipeline(user_query, thread_id):
#     """Execute the multi-agent travel planning pipeline."""
#     config = {
#         "configurable": {
#             "thread_id": thread_id
#         }
#     }
    
#     collected = {
#         "flight_results": "",
#         "hotel_results": "",
#         "itinerary": "",
#         "final_response": "",
#         "llm_calls": 0
#     }
    
#     st.markdown(
#         "<div class='section-title'>🤖 Orbit AI Pipeline</div>",
#         unsafe_allow_html=True
#     )
    
#     # Add a progress bar
#     progress_bar = st.progress(0)
#     status_text = st.empty()
    
#     try:
#         travel_graph = get_graph()
#         for i, chunk in enumerate(travel_graph.stream(
#             {
#                 "messages": [HumanMessage(content=user_query)],
#                 "user_query": user_query,
#                 "flight_results": "",
#                 "hotel_results": "",
#                 "itinerary": "",
#                 "llm_calls": 0,
#             },
#             config=config,
#             stream_mode="updates",
#         )):
#             # Update progress
#             progress = (i + 1) / 4  # Assuming 4 agents
#             progress_bar.progress(min(progress, 1.0))
            
#             for node_name, state_update in chunk.items():
#                 icon, label = AGENT_META.get(node_name, ("🔧", node_name))
#                 status_text.text(f"{icon} {label} processing...")
                
#                 with st.status(f"{icon} {label}", expanded=True, state="complete"):
#                     if node_name == "flight_agent":
#                         text = state_update.get("flight_results", "Couldn't find any relevant flight for the provided route.")
#                         collected["flight_results"] = text
#                         st.markdown(text)
                    
#                     elif node_name == "hotel_agent":
#                         text = state_update.get("hotel_results", "")
#                         collected["hotel_results"] = text
#                         st.markdown(text)
                    
#                     if node_name == "itinerary_agent":
#                         text = state_update.get("itinerary", "")
#                         collected["itinerary"] = text
#                         st.markdown(text)
                    
#                     elif node_name == "final_agent":
#                         msgs = state_update.get("messages", [])
#                         text = msgs[-1].content if msgs else ""
#                         collected["final_response"] = text
#                         st.markdown(text)
                
#                 collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])
        
#         # Clear progress indicators
#         progress_bar.empty()
#         status_text.empty()
        
#     except Exception as e:
#         st.error(f"Pipeline error: {str(e)}")
#         return
    
#     # Display metrics
#     st.markdown(
#         f"""
#         <div class='metric-wrapper'>
#             <div class='metric-card'>
#                 <div class='metric-value'>4</div>
#                 <div class='metric-label'>AI Agents</div>
#             </div>
#             <div class='metric-card'>
#                 <div class='metric-value'>{collected['llm_calls']}</div>
#                 <div class='metric-label'>LLM Calls</div>
#             </div>
#             <div class='metric-card'>
#                 <div class='metric-value'>✅</div>
#                 <div class='metric-label'>Completed</div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
    
#     # Display final response
#     st.markdown(
#         f"""
#         <div class='final-card'>
#             {collected['final_response']}
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
    
    
#     try:
#         filename, file_content = save_travel_plan(
#             user_query,
#             thread_id,
#             collected
#         )

#         # st.success("save_plan completed")

#     except Exception as e:
#             st.error(f"save_plan failed: {e}")
#             raise
    
#     st.download_button(
#         "⬇️ Download Journey",
#         data=file_content,
#         file_name=filename,
#         mime="text/markdown",
#         use_container_width=True
#     )




import streamlit as st

from langchain_core.messages import HumanMessage

from frontend.constants import AGENT_META
from frontend.utils.save_plan import save_travel_plan
from frontend.utils.graph_manager import get_graph
from frontend.utils.intent_classifier import classify_intent


def run_pipeline(user_query, trip_id, user_id):
    """Execute the multi-agent travel planning pipeline."""

    # Same thread_id formula as app.py
    thread_id = f"{user_id}::{trip_id}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print(f"DEBUG pipeline — thread_id: {thread_id}")

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

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    

    try:
        
        intent = classify_intent(user_query)
        
        st.write("DEBUG intent:", intent)
        print("DEBUG intent:", intent)
        
        if intent == "NON_TRAVEL":

                st.info(
                    """
            I'm Orbitly 🌍

            I can help with:

            ✈️ Flights
            🏨 Hotels
            🗺️ Travel Itineraries
            🌎 Destinations
            💰 Travel Budgets

            Please ask a travel-related question.
            """
                )

                return
    
        
        travel_graph = get_graph()

        for i, chunk in enumerate(travel_graph.stream(
            {
                # Only pass the new message and current query
                # Checkpointer restores all other state automatically
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "trip_intent": intent,
            },
            config=config,
            stream_mode="updates",
        )):
            progress = (i + 1) / 4
            progress_bar.progress(min(progress, 1.0))

            for node_name, state_update in chunk.items():

                print("NODE:", node_name)
                print("UPDATE:", state_update)
                
                if state_update is None:
                    print("FOUND NONE UPDATE")
                    continue
                
                
                icon, label = AGENT_META.get(node_name, ("🔧", node_name))
                status_text.text(f"{icon} {label} processing...")

                with st.status(
                    f"{icon} {label}",
                    expanded=True,
                    state="complete"
                ):
                    if node_name == "flight_agent":
                        text = state_update.get(
                            "flight_results",
                            "Couldn't find any relevant flight for the provided route."
                        )
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

                collected["llm_calls"] = state_update.get(
                    "llm_calls",
                    collected["llm_calls"]
                )

        progress_bar.empty()
        status_text.empty()

    except Exception as e:

        error_msg = str(e)

        if (
            "Request too large" in error_msg
            or "rate_limit_exceeded" in error_msg
            or "tokens per minute" in error_msg
        ):

            st.warning(
                """
    ### ⚠️ Conversation Limit Reached

    This trip conversation has become too large to process.

    Please start a **new trip chat** to continue planning.

    Creating a new chat will reset the conversation context and improve performance.
    """
            )

        else:
            st.error(f"Pipeline error: {error_msg}")

        return



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