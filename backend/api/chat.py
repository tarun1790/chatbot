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
            await asyncio.sleep(0.4) # Simulate processing
            
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
            # 2. RAG Retrieval Stage
            yield {"event": "status", "data": json.dumps({"stage": "rag_retrieval", "message": "Retrieving semantic schema, golden SQL examples, and entity matches..."})}
            await asyncio.sleep(0.5)

            # 3. Schema Selection
            yield {"event": "status", "data": json.dumps({"stage": "schema", "message": "Finding relevant tables and columns..."})}
            await asyncio.sleep(0.4)
            
            # 4. Query Planning
            yield {"event": "status", "data": json.dumps({"stage": "planning", "message": "Creating query execution plan..."})}
            await asyncio.sleep(0.4)
            
            # 5. SQL Generation
            yield {"event": "status", "data": json.dumps({"stage": "generating", "message": "Generating optimized SQL using Golden Examples..."})}
            await asyncio.sleep(0.4)
            
            # 6. Validation
            yield {"event": "status", "data": json.dumps({"stage": "validating", "message": "Validating SQL against AST security policies..."})}
            await asyncio.sleep(0.4)
            
            # 7. Execution
            yield {"event": "status", "data": json.dumps({"stage": "executing", "message": "Running secure read-only query on database..."})}
            await asyncio.sleep(0.4)
            
            # 8. Formatting Results
            yield {"event": "status", "data": json.dumps({"stage": "formatting", "message": "Formatting results and analyzing..."})}
            await asyncio.sleep(0.4)
            
            # 9. Done (Simulated result payload with RAG Context metadata)
            final_response = {
                "stage": "complete",
                "answer": f"Here is the retrieved data for your query: '{chat_req.query}'",
                "sql": "SELECT c.name, SUM(o.amount) AS total_revenue FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.name ORDER BY total_revenue DESC LIMIT 10;",
                "execution_time_ms": 142,
                "rows_returned": 3,
                "data": [
                    {"customer_name": "Acme Corp", "total_revenue": "$45,200.00"},
                    {"customer_name": "Global Tech", "total_revenue": "$38,150.00"},
                    {"customer_name": "Apex Innovations", "total_revenue": "$29,400.00"}
                ],
                "rag_context": {
                    "schema_matches": [
                        {"table": "orders", "column": "amount", "similarity_score": 0.91, "description": "Order sales revenue value"},
                        {"table": "customers", "column": "name", "similarity_score": 0.87, "description": "Customer name"}
                    ],
                    "golden_sql_matches": [
                        {"question": "Show top revenue customers", "similarity_score": 0.93, "sql": "SELECT c.name, SUM(o.amount)..."}
                    ],
                    "resolved_entities": [
                        {"input": "Hyd", "resolved_value": "Hyderabad", "similarity_score": 0.95, "field": "customers.city"}
                    ]
                }
            }
            yield {"event": "result", "data": json.dumps(final_response)}
            
        except asyncio.CancelledError:
            print("Client disconnected from stream")
            pass
        except Exception as e:
            yield {"event": "error", "data": json.dumps({"message": f"Pipeline error: {str(e)}"})}
            
    return EventSourceResponse(event_generator())
