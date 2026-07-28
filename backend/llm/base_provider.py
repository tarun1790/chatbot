from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, Optional

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate a complete string response."""
        pass

    @abstractmethod
    async def stream(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> AsyncGenerator[str, None]:
        """Stream the response chunk by chunk."""
        pass

    @abstractmethod
    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Generate a structured JSON response."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is reachable and authenticated."""
        pass
