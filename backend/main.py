from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    print("Starting Enterprise AI SQL Chatbot Backend")
    # Initialize DB pools, Schema Registry, Redis Cache
    yield
    # Shutdown actions
    print("Shutting down")

app = FastAPI(
    title="Enterprise AI SQL Chatbot",
    description="Backend API for natural language to SQL translation",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Enterprise AI SQL Chatbot Backend"}

from backend.api.chat import router as chat_router
app.include_router(chat_router)

# Include routers here (chat, database, analytics, settings) later
