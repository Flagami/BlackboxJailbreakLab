from typing import Dict, List, Any, Optional, Tuple
from utils import setup_logger

logger = setup_logger(__name__)

class CustomAPIInterface():

    def __init__(self, base_url: str, headers: Dict[str, str] = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.supported_models = []

    async def call_model(self,
                         messages: List[Dict[str, str]],
                         model_name: str,
                         **kwargs) -> Tuple[str, Dict[str, Any]]:
        import httpx

        async with httpx.AsyncClient() as client:
            payload = {
                "model": model_name,
                "messages": messages,
                **kwargs
            }

            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )

            result = response.json()
            return result["content"], result.get("metadata", {})

    def get_supported_models(self) -> List[str]:
        return self.supported_models