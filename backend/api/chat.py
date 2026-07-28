import json
import asyncio
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

# Simplified imports for brevity
from backend.llm.system_prompts import IRRELEVANT_REJECTION_MESSAGE

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
            
            # SIMULATE INTENT CLASSIFIER CATEGORY_D (Irrelevant Questions)
            irrelevant_keywords = ["joke", "python", "tesla", "match", "capital", "translate", "image"]
            is_irrelevant = any(kw in chat_req.query.lower() for kw in irrelevant_keywords)
            
            if is_irrelevant:
                # Short-circuit the pipeline immediately
                final_response = {
                    "stage": "complete",
                    "answer": IRRELEVANT_REJECTION_MESSAGE,
                    "sql": None,
                    "execution_time_ms": 50,
                    "rows_returned": 0,
                    "data": []
                }
                yield {"event": "result", "data": json.dumps(final_response)}
                return

            # Continue Normal Pipeline for Category A
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
            print("Client disconnected from stream")
            pass
        except Exception as e:
            yield {"event": "error", "data": json.dumps({"message": f"Pipeline error: {str(e)}"})}
            
    return EventSourceResponse(event_generator())
