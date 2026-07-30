from typing import Dict, Any, List
from backend.services.rag_engine import RAGEngine

class SchemaSelector:
    def __init__(self, schema_registry, rag_engine: RAGEngine = None):
        self.schema_registry = schema_registry
        self.rag_engine = rag_engine

    async def select_relevant_schema(self, intent_data: Dict[str, Any], user_query: str = "", max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Retrieves relevant schema using Vector RAG semantic search combined with the Schema Registry.
        """
        full_schema = await self.schema_registry.get_schema()
        relevant_tables = set(intent_data.get("tables", []))

        # Perform RAG-guided schema retrieval if RAGEngine is attached
        rag_schema_matches = []
        if self.rag_engine and user_query:
            rag_schema_matches = self.rag_engine.retrieve_relevant_schema_context(user_query)
            for match in rag_schema_matches:
                if "table" in match and match["table"]:
                    relevant_tables.add(match["table"])

        compressed_schema = {
            "tables": {},
            "relationships": [],
            "rag_matches": rag_schema_matches
        }

        if not relevant_tables:
            compressed_schema["tables"] = full_schema.get("tables", {})
            compressed_schema["relationships"] = full_schema.get("relationships", [])
        else:
            for table in relevant_tables:
                if table in full_schema.get("tables", {}):
                    compressed_schema["tables"][table] = full_schema["tables"][table]

            compressed_schema["relationships"] = [
                rel for rel in full_schema.get("relationships", [])
                if rel.get("table") in relevant_tables and rel.get("referenced_table") in relevant_tables
            ]

        return compressed_schema
