---
title: Orbitly
emoji: 🌌
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8501
pinned: false
---

# 🌍 Orbitly – AI Travel Planning Assistant

Orbitly is a multi-agent AI travel planner that helps users create, modify, and extend personalized travel itineraries using LLM-powered reasoning, flight discovery, hotel recommendations, and travel intelligence.

**Live Demo:** https://rajcby-orbitly.hf.space

---

## ✨ Features

### 🧠 Intelligent Travel Planning

* Generate complete travel itineraries
* Plan trips based on destination, budget, and duration
* Get personalized recommendations

### ✈️ Flight Discovery

* Search and recommend relevant flight options
* Integrates external travel APIs for flight information

### 🏨 Hotel Recommendations

* Discover hotels and accommodations
* Curated using live web search

### 🔄 Multi-Agent Workflow

Orbitly uses a LangGraph-powered multi-agent architecture:

1. Intent Agent
2. Flight Agent
3. Hotel Agent
4. Itinerary Agent
5. Final Concierge Agent

Each agent performs a dedicated task and contributes to the final travel plan.

### 📝 Trip Modification Support

Users can:

* Create new trips
* Add destinations to existing trips
* Modify budgets, activities, and preferences

### 💾 Persistent Conversation Memory

* PostgreSQL Checkpointer
* Conversation history stored using LangGraph checkpoints
* Supports long-running travel planning sessions

### 📥 Export Travel Plans

* Download generated itineraries
* Save trip plans for future reference

---

## 🏗️ Architecture

```text
User Query
     │
     ▼
Intent Agent
     │
     ▼
Flight Agent
     │
     ▼
Hotel Agent
     │
     ▼
Itinerary Agent
     │
     ▼
Final Concierge Agent
     │
     ▼
Final Travel Plan
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### AI & Orchestration

* LangGraph
* LangChain
* Groq LLM
* Llama 3.3 70B Versatile

### Search & Travel Intelligence

* Tavily Search API
* Flight Search API

### Database

* PostgreSQL
* LangGraph Postgres Checkpointer

### Deployment

* Docker
* Hugging Face Spaces

---

## 📂 Project Structure

```text
Orbitly/
│
├── app.py
├── graph/
│   └── travel_graph.py
│
├── frontend/
│   ├── components/
│   ├── utils/
│   └── constants.py
│
├── tools/
│   ├── flight_tool.py
│   └── tavily_tool.py
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_key

TAVILY_API_KEY=your_tavily_key

DATABASE_URL=postgresql://username:password@host:port/database
```

---

## 🚀 Local Setup

### 1. Clone Repository

```bash
git clone <repository-url>

cd Orbitly
```

### 2. Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
streamlit run app.py
```

---

## 🐳 Docker Deployment

Build Image:

```bash
docker build -t orbitly .
```

Run Container:

```bash
docker run -p 8501:8501 \
-e GROQ_API_KEY=xxxxx \
-e TAVILY_API_KEY=xxxxx \
-e DATABASE_URL=xxxxx \
orbitly
```

---

## 🌐 Hugging Face Deployment

Orbitly is deployed on Hugging Face Spaces:

https://rajcby-orbitly.hf.space

---

## 🔮 Future Enhancements

* Real-time flight pricing
* Hotel booking integrations
* Visa requirement assistance
* Interactive travel maps
* Multi-user trip collaboration
* Cost optimization recommendations
* Travel document generation

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

## 👨‍💻 Author

Raj Chakraborty

Software Engineer | Automation Engineer | AI Enthusiast

## 📜 License

MIT License

---

Built with ❤️ using LangGraph, Groq, PostgreSQL, and Streamlit.
