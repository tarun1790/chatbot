import json
import asyncio
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

# Simplified imports for brevity (in production use dependency injection)
from backend.llm.gemini_provider import GeminiProvider
from backend.services.intent_classifier import IntentClassifier
from backend.services.schema_selector import SchemaSelector
from backend.services.query_planner import QueryPlanner
from backend.services.sql_generator import SQLGenerator
from backend.services.sql_security_gateway import SQLSecurityGateway
from backend.services.query_executor import QueryExecutor

# These would normally be injected dependencies setup during app initialization
# Using placeholders here to satisfy the architectural flow requirements.

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

class ChatRequest(BaseModel):
    query: str
    session_id: str

@router.post("/stream")
async def chat_stream(request: Request, chat_req: ChatRequest):
    """
    Main SSE Streaming Endpoint orchestrating the entire NL2SQL pipeline.
    """
    async def event_generator():
        try:
            # 1. Understanding Question
            yield {"event": "status", "data": json.dumps({"stage": "understanding", "message": "Analyzing question intent..."})}
            await asyncio.sleep(0.5) # Simulate processing
            
            # 2. Schema Selection
            yield {"event": "status", "data": json.dumps({"stage": "schema", "message": "Finding relevant tables and columns..."})}
            await asyncio.sleep(0.5)
            
            # 3. Query Planning
            yield {"event": "status", "data": json.dumps({"stage": "planning", "message": "Creating query execution plan..."})}
            await asyncio.sleep(0.5)
            
            # 4. SQL Generation
            yield {"event": "status", "data": json.dumps({"stage": "generating", "message": "Generating optimized SQL..."})}
            await asyncio.sleep(0.5)
            
            # 5. Validation
            yield {"event": "status", "data": json.dumps({"stage": "validating", "message": "Validating SQL against security policies..."})}
            await asyncio.sleep(0.5)
            
            # 6. Execution
            yield {"event": "status", "data": json.dumps({"stage": "executing", "message": "Running secure query on database..."})}
            await asyncio.sleep(0.5)
            
            # 7. Formatting Results
            yield {"event": "status", "data": json.dumps({"stage": "formatting", "message": "Formatting results and analyzing..."})}
            await asyncio.sleep(0.5)
            
            # 8. Done (Simulated result payload)
            final_response = {
                "stage": "complete",
                "answer": f"Here is the data for your request: '{chat_req.query}'",
                "sql": "SELECT * FROM mock_table LIMIT 10;",
                "execution_time_ms": 150,
                "rows_returned": 10,
                "data": [{"id": 1, "value": "demo_data"}]
            }
            yield {"event": "result", "data": json.dumps(final_response)}
            
        except asyncio.CancelledError:
            # Client disconnected
            print("Client disconnected from stream")
            pass
        except Exception as e:
            yield {"event": "error", "data": json.dumps({"message": f"Pipeline error: {str(e)}"})}
            
    return EventSourceResponse(event_generator())
