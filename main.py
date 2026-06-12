import os
import operator
from typing import TypedDict, Annotated

import psycopg

from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flight


# ==========================
# LOAD ENV
# ==========================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ==========================
# LLM
# ==========================

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

# ==========================
# STATE
# ==========================

class TravelState(TypedDict):

    messages: Annotated[list[AnyMessage], operator.add]

    user_query: str

    trip_intent: str

    flight_results: str

    hotel_results: str

    itinerary: str

    llm_calls: int


# ==========================
# INTENT AGENT
# ==========================

def intent_agent(state: TravelState):

    query = state["user_query"]

    response = llm.invoke([
        SystemMessage(
            content="""
You are an intent classifier.

Classify the user's request into one of:

NEW_TRIP
- planning a completely new vacation
- new destination unrelated to current itinerary

ADD_DESTINATION
- add a city
- add a destination
- include another stop
- extend itinerary
- spend time in another location
- also visit
- include
- add
- cover

MODIFY_TRIP
- change budget
- modify schedule
- remove activities
- replace hotel
- adjust itinerary

Return ONLY:

NEW_TRIP
ADD_DESTINATION
MODIFY_TRIP
"""
),
        HumanMessage(content=query)
    ])

    return {
        "trip_intent": response.content.strip(),
        "llm_calls": state.get("llm_calls", 0) + 1
    }




# ==========================
# FLIGHT AGENT
# ==========================

def flight_agent(state: TravelState):

    query = state["user_query"]

    flight_data = search_flight(query)

    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content="Flight information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ==========================
# HOTEL AGENT
# ==========================

def hotel_agent(state: TravelState):

    query = f"Best hotels and hostels for {state['user_query']}"

    hotel_result = tavily_search(query)

    return {
        "hotel_results": hotel_result,
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ==========================
# ITINERARY AGENT
# ==========================

def itinerary_agent(state: TravelState):

    history = "\n".join(
        [
            msg.content
            for msg in state.get("messages", [])
            if hasattr(msg, "content")
        ]
    )

    prompt = f"""
    Previous Conversation:

    {history}

    Current Request:
    {state['user_query']}

    Intent:
    {state['trip_intent']}

    Flight Information:
    {state['flight_results']}

    Hotel Information:
    {state['hotel_results']}

    Rules:

    If intent is NEW_TRIP:
    - Create a completely new itinerary.

    If intent is ADD_DESTINATION:
    - Keep all existing destinations.
    - Add the newly requested destination.
    - Rebalance the days accordingly.

    If intent is MODIFY_TRIP:
    - Modify the existing itinerary.
    - Preserve existing destinations unless explicitly removed.

    Return a complete updated itinerary.
    """

    response = llm.invoke([
        SystemMessage(
            content="You are an expert travel planner."
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ==========================
# FINAL AGENT
# ==========================

def final_agent(state: TravelState):

    final_prompt = f"""
Create a polished final travel plan.

Flights:
{state['flight_results']}

Hotels:
{state['hotel_results']}

Itinerary:
{state['itinerary']}
"""

    response = llm.invoke([
        SystemMessage(
            content="You are a premium travel concierge."
        ),
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ==========================
# ROUTER
# ==========================

def route_trip(state: TravelState):

    intent = state["trip_intent"]

    if intent == "ADD_DESTINATION":
        return "add_destination"

    if intent == "MODIFY_TRIP":
        return "modify_trip"

    return "new_trip"


# ==========================
# GRAPH
# ==========================

graph = StateGraph(TravelState)

graph.add_node("intent_agent", intent_agent)

graph.add_node("flight_agent", flight_agent)

graph.add_node("hotel_agent", hotel_agent)

graph.add_node("itinerary_agent", itinerary_agent)

graph.add_node("final_agent", final_agent)


graph.add_edge(START, "intent_agent")

graph.add_conditional_edges(
    "intent_agent",
    route_trip,
    {
        "new_trip": "flight_agent",
        "add_destination": "hotel_agent",
        "modify_trip": "hotel_agent"
    }
)

graph.add_edge("flight_agent", "hotel_agent")

graph.add_edge("hotel_agent", "itinerary_agent")

graph.add_edge("itinerary_agent", "final_agent")

graph.add_edge("final_agent", END)

# ==========================
# POSTGRES CHECKPOINTER
# ==========================

_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True
)

checkpointer = PostgresSaver(_conn)

# checkpointer.setup()

# ==========================
# COMPILE GRAPH
# ==========================

app = graph.compile(
    checkpointer=checkpointer
)

# ==========================
# LOCAL TESTING
# ==========================

if __name__ == "__main__":

    trip_id = input("Trip ID: ")

    user_input = input("Travel Request: ")

    config = {
        "configurable": {
            "thread_id": trip_id
        }
    }

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "trip_intent": "",
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )

    print("\nFinal Response:\n")

    for msg in result["messages"]:

        print(msg.content)

        print(
            "\n----------------------------------\n"
        )