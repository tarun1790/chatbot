import json
import google.generativeai as genai
from typing import Any, AsyncGenerator, Dict, Optional
from backend.llm.base_provider import BaseLLMProvider

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model_name: str = "models/gemini-2.5-flash"):
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(self.model_name)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        # Note: In a production environment with the latest SDK, system_instruction is supported natively
        # For simplicity here we prepend the system prompt if available.
        full_prompt = f"System: {system_prompt}\n\nUser: {prompt}" if system_prompt else prompt
        response = await self.model.generate_content_async(full_prompt)
        return response.text

    async def stream(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> AsyncGenerator[str, None]:
        full_prompt = f"System: {system_prompt}\n\nUser: {prompt}" if system_prompt else prompt
        response = await self.model.generate_content_async(full_prompt, stream=True)
        async for chunk in response:
            yield chunk.text

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        # Using Gemini's JSON mode if available, or extracting JSON block
        full_prompt = f"System: {system_prompt}\n\nYou MUST return ONLY valid JSON.\nUser: {prompt}" if system_prompt else prompt
        response = await self.model.generate_content_async(full_prompt)
        text = response.text
        
        # Strip markdown formatting if present
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        return json.loads(text.strip())

    async def health_check(self) -> bool:
        try:
            # Simple list models to verify API key
            models = genai.list_models()
            return any(m.name == self.model_name for m in models)
        except Exception:
            return False
