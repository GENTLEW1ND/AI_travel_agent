import os
from datetime import datetime


def save_travel_plan(user_query, thread_id, collected):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"orbitly_plan_{timestamp}.md"

    save_dir = "travel_plans"

    os.makedirs(save_dir, exist_ok=True)

    file_content = f"""
# Orbitly Travel Plan

## Query
{user_query}

## User
{thread_id}

---

## Flights
{collected['flight_results']}

---

## Hotels
{collected['hotel_results']}

---

## Itinerary
{collected['itinerary']}

---

## Final Plan
{collected['final_response']}
"""

    path = os.path.join(save_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(file_content)

    return filename, file_content
