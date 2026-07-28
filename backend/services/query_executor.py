import time
from typing import Dict, Any
from backend.database.base_adapter import BaseDatabaseAdapter

class QueryExecutor:
    def __init__(self, db_adapter: BaseDatabaseAdapter):
        self.db = db_adapter

    async def execute(self, safe_sql: str) -> Dict[str, Any]:
        """
        Executes a validated, sanitized SQL query against the database.
        Captures telemetry and ensures safe error handling.
        """
        start_time = time.time()
        try:
            results = await self.db.execute_query(safe_sql)
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "data": results,
                "row_count": len(results),
                "execution_time_ms": round(execution_time * 1000, 2)
            }
        except Exception as e:
            execution_time = time.time() - start_time
            # Return safe error representation, do not leak raw stack traces
            return {
                "success": False,
                "error": "Database execution failed.",
                "details": str(e),
                "execution_time_ms": round(execution_time * 1000, 2)
            }
