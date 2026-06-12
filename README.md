---
title: Orbitly
emoji: 🌌
colorFrom: blue
colorTo: purple
pinned: false
---

# 🌌 Orbitly – AI Multi-Agent Travel Planner

Orbitly is an AI-powered travel planning assistant built using LangGraph, Groq LLMs, PostgreSQL, Tavily Search, and Streamlit.

The application uses multiple specialized AI agents to collaboratively generate personalized travel itineraries, discover accommodations, retrieve travel information, and maintain conversation history across trips.

---

## 🚀 Features

### ✈️ Multi-Agent Architecture

Orbitly uses a coordinated AI agent workflow:

* Flight Agent

  * Finds flight information for the destination.

* Hotel Agent

  * Searches for accommodation recommendations.

* Itinerary Agent

  * Creates detailed travel itineraries.

* Orbit Core

  * Generates the final travel plan.

---

### 🧠 Persistent Trip Memory

Each trip is assigned a unique thread ID.

Examples:

* delhi_9d68cfdf
* japan_bdc4917b
* singapore_7ac1f0d2

Conversation history is stored in PostgreSQL using LangGraph Checkpointing.

Users can:

* Create multiple trips
* Switch between trips
* Continue planning existing trips
* Maintain separate travel memories

---

### 🔄 Context-Aware Planning

Orbitly identifies user intent and supports:

#### New Trip

Example:

Plan a 7-day trip to Delhi from Shillong

#### Add Destination

Example:

Add Rishikesh to the itinerary

#### Modify Trip

Example:

Reduce the budget
Change hotels
Add more activities

The assistant updates existing plans while preserving previous context.

---

## 🏗️ Architecture

User Input

↓

Intent Agent

↓

Router

↓

Flight Agent

↓

Hotel Agent

↓

Itinerary Agent

↓

Final Agent

↓

PostgreSQL Checkpointer

---

## 🛠️ Tech Stack

### AI & LLM

* LangGraph
* LangChain
* Groq
* LLaMA 3.3 70B

### Frontend

* Streamlit

### Database

* PostgreSQL
* LangGraph Checkpointing

### Search & Retrieval

* Tavily Search API

### Flight Search

* Aviation APIs

---

## 📂 Project Structure

```text
TravelAIAssistant/

├── app.py

├── main.py

├── frontend/
│   ├── components/
│   ├── styles/
│   └── utils/

├── tools/
│   ├── flight_tool.py
│   └── tavily_tool.py

├── .env

├── requirements.txt

└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_key

TAVILY_API_KEY=your_tavily_key

DATABASE_URL=postgresql://username:password@localhost:5432/orbitly
```

---

## 🐘 PostgreSQL Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE orbitly;
```

Create a trips table:

```sql
CREATE TABLE trips (
    trip_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    destination VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

LangGraph automatically creates:

* checkpoints
* checkpoint_blobs
* checkpoint_writes
* checkpoint_migrations

during startup.

---

## ▶️ Run Locally

Create virtual environment:

```bash
python -m venv Langgraph_venv
```

Activate:

Linux / Mac

```bash
source Langgraph_venv/bin/activate
```

Windows

```bash
Langgraph_venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

---

## 🌍 Example Workflow

1. Create a trip

Destination:
Delhi

2. Generate itinerary

Plan a 7-day trip to Delhi from Shillong

3. Continue conversation

Add Rishikesh to the itinerary

4. Switch trips

Japan
Singapore
Bali

Each trip maintains independent memory.

---

## 📈 Future Enhancements

* Real-time flight pricing
* Weather intelligence agent
* Restaurant recommendation agent
* Budget optimization agent
* Interactive maps
* PDF itinerary export
* Multi-user authentication
* Vector database memory

---

## 🤝 Contributions

Contributions, issues, and feature requests are welcome.

Feel free to fork the repository and submit pull requests.

---

## 📜 License

MIT License

---

Built with ❤️ using LangGraph, Groq, PostgreSQL, and Streamlit.
