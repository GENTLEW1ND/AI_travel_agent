from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

def classify_intent(query):

    response = llm.invoke([
        SystemMessage(
            content="""
Return ONLY one of:

NEW_TRIP
ADD_DESTINATION
MODIFY_TRIP
NON_TRAVEL

NEW_TRIP:
- plan a trip
- itinerary
- vacation
- travel planning

ADD_DESTINATION:
- add a city
- include another destination
- extend itinerary

MODIFY_TRIP:
- change budget
- modify itinerary
- replace hotels
- remove activities

NON_TRAVEL:
- greetings
- coding questions
- random text
- unrelated requests
"""
        ),
        HumanMessage(content=query)
    ])

    return response.content.strip().upper()