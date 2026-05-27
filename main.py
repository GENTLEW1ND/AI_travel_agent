import os
from typing import TypedDict, Annotated
import operator

import psycopg
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)

from langchain_groq import ChatGroq

from dotenv import load_dotenv


from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flight

load_dotenv()


llm = ChatGroq(
    model = "llama-3.3-70b-versatile"
)

DATABASE_URL = os.getenv("DATABASE_URL")



class TravelState(TypedDict):
    message: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
    
def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flight(query)
    
    return{
        "flight_results" : flight_data,
        "message": [
            AIMessage(content = f"Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
    
def hotel_agent(state: TravelState):
    query = f"Best hostels for {state["user_query"]}"
    hotel_result = tavily_search(query)
    
    return{
        "hotel_results" : hotel_result,
        "message": [
            AIMessage(content = f"Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
    
def itinerary_agent(state: TravelState):
    prompt = f"""
        Create a travel itinerary,
        User Query:
        {state['user_query']}
        
        Flight Results:
        {state['flight_results']}
        
        Hotel Results:
        {state['hotel_results']}
    """
    response = llm.invoke({
        SystemMessage(
            content = "You are an expernt travel planner"
        ),
        HumanMessage(content=prompt)
    })
    
    return{
        "Itinerary" : response.content,
        "message": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
    
def final_agent(state: TravelState):
    final_prompt = f"""
        Generate final travel response,
        Flights:
        {state['flight_results']}
        
        Hotels:
        {state['hotel_results']}
        
        Itinerary:
        {state['itinerary']}
    """
    response = llm.invoke({
        HumanMessage(content=final_prompt)
    })
    
    return{
        "message": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
    
#Creating the graph for langgraph    
graph = StateGraph(TravelState)
#Creating the nodes
graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinenary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)
#Creating the edges
graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)


##Working the with the database for chat history
_conn = psycopg.connect(DATABASE_URL)
checkpointer = PostgresSaver(_conn)
checkpointer.setup()


##Compiling the langgraph
app = graph.compile(checkpointer=checkpointer)