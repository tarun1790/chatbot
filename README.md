# Enterprise AI SQL Chatbot Dashboard

A production-ready Enterprise AI SQL Chatbot Dashboard capable of answering natural-language questions over a company's MySQL database using an advanced Schema-Aware Text-to-SQL Pipeline.

## Features
- **No Vector Database**: Uses an intelligent Schema Registry and SQL Generator for 100% accurate structured data retrieval.
- **SQL Security Gateway**: Strict AST-based parsing (via SQLGlot) to block all destructive operations (DROP, INSERT, UPDATE, etc).
- **SSE Streaming Chat**: Real-time pipeline execution updates in the UI.
- **Luxury Enterprise Theme**: Premium React dashboard with dark/gold aesthetics.
- **Modular Services**: Highly decoupled FastAPI backend.

## Quick Start (Docker)

1. Rename `.env.example` to `.env` and fill in your Gemini/OpenAI API Keys.
2. Run the entire stack using Docker Compose:

```bash
docker compose up --build
```

### Accessing the Applications
- **Frontend Dashboard**: [http://localhost:5173](http://localhost:5173)
- **FastAPI Backend (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Project Structure
- `/frontend`: React 18, Vite, Tailwind CSS v4, Lucide React, Framer Motion.
- `/backend`: FastAPI, SQLAlchemy, SQLGlot, AI pipeline services.
- `/docker-compose.yml`: Local orchestrator for frontend, backend, MySQL, and Redis.

## Testing
To run the SQL Security Gateway unit tests:
```bash
cd backend
pytest tests/
```
