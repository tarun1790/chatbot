from typing import Dict, Any
from backend.llm.base_provider import BaseLLMProvider
from backend.llm.system_prompts import MASTER_SYSTEM_PROMPT, INTENT_CLASSIFIER_PROMPT

class IntentClassifier:
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm = llm_provider
        self.system_prompt = f"{MASTER_SYSTEM_PROMPT}\n\n{INTENT_CLASSIFIER_PROMPT}"

    async def classify(self, user_query: str) -> Dict[str, Any]:
        """Classifies the intent of the user's question into Categories A-D."""
        try:
            result = await self.llm.generate_json(
                prompt=user_query,
                system_prompt=self.system_prompt
            )
            
            # Ensure safe fallback formatting
            category = result.get("category", "CATEGORY_A")
            confidence = result.get("confidence", 50.0)
            
            return {"category": category, "confidence": confidence}
        except Exception as e:
            # On failure, assume it's a data query but with low confidence
            return {"category": "CATEGORY_A", "confidence": 10.0, "error": str(e)}
