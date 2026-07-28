from typing import Dict, Any
from backend.llm.base_provider import BaseLLMProvider
from backend.llm.system_prompts import MASTER_SYSTEM_PROMPT, SQL_GENERATOR_PROMPT

class SQLGenerator:
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm = llm_provider
        self.system_prompt = f"{MASTER_SYSTEM_PROMPT}\n\n{SQL_GENERATOR_PROMPT}\n\nDO NOT include markdown formatting (like ```sql) in the output, JUST the raw SQL."

    async def generate_sql(self, query_plan: Dict[str, Any], compressed_schema: Dict[str, Any]) -> str:
        """Generates raw SQL from the query plan."""
        prompt = f"Query Plan:\n{query_plan}\n\nSchema Context:\n{compressed_schema}\n\nGenerate the ANSI-compliant read-only SQL query now:"
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
