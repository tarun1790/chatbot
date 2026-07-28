from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseDatabaseAdapter(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_tables(self) -> List[str]:
        pass

    @abstractmethod
    async def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_foreign_keys(self) -> List[Dict[str, Any]]:
        pass
