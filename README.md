# AI Gym Membership & Trainer Booking Assistant

This is a production-ready, clean-architecture backend service for an AI Gym Membership & Trainer Booking Assistant. It manages member registrations, personal trainer session bookings, membership plans, and uses Retrieval-Augmented Generation (RAG) to answer questions without hallucination.

The application is built with **Python 3.12**, **FastAPI**, **MySQL**, **SQLAlchemy**, and integrates with **Ollama** running **Llama 3**.

---

## Key Features

1. **Clean Architecture**: Strictly organized into domain models, data transfer schemas (Pydantic), repositories (data-access layer), services (business layer), and routers (presentation layer).
2. **Repository & Service Patterns**: Decouples business rules from database access, allowing easy maintenance and testing.
3. **Conversational History Context**: Retrieves the last 10 messages of conversation history per session to provide context to the LLM.
4. **Gym Fact RAG Search**: Matches user queries using database search over membership plans and trainers, passing them as prompt context.
5. **No Hallucination Prompting**: Strictly constrains the model to only answer using provided database facts.
6. **Auto-Booking & Identification Tagging**: Intercepts structured JSON outputs from Llama 3 to automatically book trainers and identify/register gym members on-the-fly.
7. **Complete Mock Test Coverage**: Integration and unit tests using SQLite in-memory, decoupled from active MySQL/Ollama requirements.

---

## Directory Structure

```
/
├── app/
│   ├── exceptions/            # Global API Exception handler
│   ├── models/                # SQLAlchemy Entity Models
│   ├── schemas/               # Pydantic Request/Response validation Schemas
│   ├── repositories/          # Repository Pattern
│   ├── services/              # Service Layer (business logic & Ollama API)
│   ├── routers/               # FastAPI endpoints
│   ├── config.py              # Settings loader using Pydantic Settings
│   ├── database.py            # SQLAlchemy Connection management
│   └── main.py                # Main application server & logger
├── docker/
│   ├── app.Dockerfile         # FastAPI application Docker container
│   └── docker-compose.yml     # Multi-container orchestration (MySQL + Ollama + App)
├── sql/
│   └── schema.sql             # Raw DDL SQL script and initial seeds
├── tests/
│   ├── conftest.py            # SQLite database fixtures and Ollama mocks
│   └── test_chatbot.py        # Conversational integration tests
├── .env.example               # Environment variables template
├── requirements.txt           # Python application requirements
└── README.md                  # Setup & Architecture document
```

---

## Setup & Running Guide

### Method A: Running with Docker (Recommended)

This compiles and runs the entire stack (FastAPI App, MySQL database, and Ollama) using docker compose.

1. **Start the containers**:
   ```bash
   docker-compose -f docker/docker-compose.yml up -d --build
   ```

2. **Pull the Llama 3 model** inside the Ollama container:
   ```bash
   docker exec -it ollama_service ollama pull llama3
   ```

3. **Verify the Application**:
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to view the OpenAPI Swagger documentation.

---

### Method B: Running Locally

#### 1. Setup Database
Ensure you have a MySQL server running locally. Create a database named `gym_db`:
```sql
CREATE DATABASE gym_db;
```
*(Optional: Run `sql/schema.sql` to pre-seed the database, otherwise the application auto-creates the tables and schema on startup).*

#### 2. Run Ollama Locally
1. Download Ollama from [ollama.com](https://ollama.com).
2. Start the Ollama server:
   ```bash
   ollama serve
   ```
3. Pull the Llama 3 model:
   ```bash
   ollama pull llama3
   ```

#### 3. Install Python Dependencies
Create a virtual environment and install the required modules:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Copy `.env.example` to `.env` and verify the values match your local database and Ollama setups.
```bash
cp .env.example .env
```

#### 5. Run FastAPI App
```bash
python -m app.main
```
The server will start on [http://localhost:8000](http://localhost:8000).

---

## Running Unit and Integration Tests

To execute the tests:
```bash
pytest -v
```
