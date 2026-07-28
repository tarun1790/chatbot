import json
from typing import Dict, Any, List
from backend.database.base_adapter import BaseDatabaseAdapter
import redis.asyncio as redis

class SchemaRegistry:
    def __init__(self, db_adapter: BaseDatabaseAdapter, redis_url: str):
        self.db = db_adapter
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.schema_key = "enterprise:schema_registry"

    async def introspect_and_cache(self) -> Dict[str, Any]:
        """Introspects the database and updates the schema registry in Redis."""
        tables = await self.db.get_tables()
        
        schema_data = {
            "version": 1,
            "tables": {},
            "relationships": []
        }

        for table in tables:
            table_info = await self.db.get_table_schema(table)
            schema_data["tables"][table] = table_info

        fks = await self.db.get_foreign_keys()
        schema_data["relationships"] = fks

        # Save to Redis
        await self.redis_client.set(self.schema_key, json.dumps(schema_data))
        return schema_data

    async def get_schema(self) -> Dict[str, Any]:
        """Retrieves the cached schema, or introspects if not available."""
        data = await self.redis_client.get(self.schema_key)
        if data:
            return json.loads(data)
        return await self.introspect_and_cache()
