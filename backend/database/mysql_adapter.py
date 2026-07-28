import aiomysql
from typing import Any, Dict, List, Optional
from backend.database.base_adapter import BaseDatabaseAdapter

class MySQLAdapter(BaseDatabaseAdapter):
    def __init__(self, host, port, user, password, db_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.pool: Optional[aiomysql.Pool] = None

    async def connect(self) -> None:
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db_name,
            autocommit=True
        )

    async def disconnect(self) -> None:
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not self.pool:
            raise Exception("Database not connected")
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params or {})
                return await cur.fetchall()

    async def get_tables(self) -> List[str]:
        query = "SHOW TABLES"
        results = await self.execute_query(query)
        tables = []
        for row in results:
            tables.append(list(row.values())[0])
        return tables

    async def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        query = f"DESCRIBE {table_name}"
        columns = await self.execute_query(query)
        return {"columns": columns}

    async def get_foreign_keys(self) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                TABLE_NAME as 'table',
                COLUMN_NAME as 'column',
                REFERENCED_TABLE_NAME as 'referenced_table',
                REFERENCED_COLUMN_NAME as 'referenced_column'
            FROM 
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE 
                REFERENCED_TABLE_SCHEMA = %s;
        """
        return await self.execute_query(query, {"db_name": self.db_name})
