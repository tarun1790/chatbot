from typing import Dict, Any
from backend.llm.base_provider import BaseLLMProvider

class SQLGenerator:
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm = llm_provider
        self.system_prompt = """
        You are an expert SQL Generator.
        Given a structured query plan and the relevant database schema, generate a safe, optimized, ANSI-compliant MySQL query.
        
        Rules:
        1. Only generate SELECT queries. NEVER generate INSERT, UPDATE, DELETE, or DROP.
        2. Use the provided query plan structure as a blueprint.
        3. Ensure table aliases are used correctly.
        4. Do NOT include markdown formatting (like ```sql) in the output, JUST the raw SQL.
        5. ALWAYS add a LIMIT if the query could return many rows.
        """

    async def generate_sql(self, query_plan: Dict[str, Any], compressed_schema: Dict[str, Any]) -> str:
        """Generates raw SQL from the query plan."""
        prompt = f"Query Plan:\n{query_plan}\n\nSchema Context:\n{compressed_schema}\n\nGenerate the SQL query now:"
        try:
            sql = await self.llm.generate(
                prompt=prompt,
                system_prompt=self.system_prompt
            )
            # Clean up markdown formatting if the LLM ignored instructions
            sql = sql.strip()
            if sql.startswith("```sql"):
                sql = sql[6:]
            if sql.startswith("```"):
                sql = sql[3:]
            if sql.endswith("```"):
                sql = sql[:-3]
                
            return sql.strip()
        except Exception as e:
            raise Exception(f"Failed to generate SQL: {e}")
