from typing import Dict, Any, List

class SchemaSelector:
    def __init__(self, schema_registry):
        self.schema_registry = schema_registry

    async def select_relevant_schema(self, intent_data: Dict[str, Any], max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Compresses the full schema into only the relevant tables/columns based on the intent.
        """
        full_schema = await self.schema_registry.get_schema()
        
        # In a real implementation, we would use NLP/Embeddings or exact keyword matching 
        # to filter out irrelevant tables from `full_schema`. 
        # For this prototype, we'll return a compressed version of everything if it fits,
        # or just the identified tables from the query planner/intent.
        
        relevant_tables = intent_data.get("tables", [])
        
        compressed_schema = {
            "tables": {},
            "relationships": []
        }
        
        if not relevant_tables:
            # If no specific tables identified, return all (up to a limit)
            compressed_schema = full_schema
        else:
            for table in relevant_tables:
                if table in full_schema["tables"]:
                    compressed_schema["tables"][table] = full_schema["tables"][table]
                    
            # Filter relationships where both tables are in our relevant set
            compressed_schema["relationships"] = [
                rel for rel in full_schema.get("relationships", [])
                if rel["table"] in relevant_tables and rel["referenced_table"] in relevant_tables
            ]
            
        return compressed_schema
