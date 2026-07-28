from typing import Dict, Any
from backend.llm.base_provider import BaseLLMProvider

class QueryPlanner:
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm = llm_provider
        self.system_prompt = """
        You are an expert SQL Query Planner.
        Given a user query and a compressed database schema, create a structured query plan.
        
        The query plan MUST be a JSON object containing:
        {
            "intent": "aggregate_metric | raw_data | comparison",
            "tables": ["table1", "table2"],
            "joins": [{"from": "table1.id", "to": "table2.table1_id"}],
            "metrics": ["SUM(table1.amount)"],
            "dimensions": ["table2.name"],
            "filters": [{"column": "table2.name", "operator": "=", "value": "Example"}],
            "group_by": ["table2.name"],
            "sort_by": [{"column": "SUM(table1.amount)", "order": "DESC"}],
            "limit": 100
        }
        """

    async def create_plan(self, user_query: str, compressed_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Creates an intermediate structured query plan before generating SQL."""
        prompt = f"User Query: {user_query}\n\nSchema Context:\n{compressed_schema}"
        try:
            plan = await self.llm.generate_json(
                prompt=prompt,
                system_prompt=self.system_prompt
            )
            return plan
        except Exception as e:
            raise Exception(f"Failed to generate query plan: {e}")
