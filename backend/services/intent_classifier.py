from typing import Dict, Any
from backend.llm.base_provider import BaseLLMProvider

class IntentClassifier:
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm = llm_provider
        self.system_prompt = """
        You are an expert intent classifier for a data querying system.
        Classify the user's intent into one of the following categories:
        - 'data_query' : Asking for specific data, aggregations, or reports.
        - 'schema_inquiry' : Asking about what data is available or how it is structured.
        - 'general_chat' : Greetings or non-data related queries.
        
        Return a JSON object with 'intent' (string) and 'confidence' (float 0.0 - 1.0).
        """

    async def classify(self, user_query: str) -> Dict[str, Any]:
        """Classifies the intent of the user's question."""
        try:
            result = await self.llm.generate_json(
                prompt=user_query,
                system_prompt=self.system_prompt
            )
            return result
        except Exception as e:
            # Fallback to data_query on failure
            return {"intent": "data_query", "confidence": 0.5, "error": str(e)}
