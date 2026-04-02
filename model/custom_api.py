from typing import Dict, List, Any, Optional, Tuple
# 自定义库
from utils import setup_logger

logger = setup_logger(__name__)

class CustomAPIInterface():
    """自定义API接口"""

    def __init__(self, base_url: str, headers: Dict[str, str] = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.supported_models = []

    async def call_model(self,
                         messages: List[Dict[str, str]],
                         model_name: str,
                         **kwargs) -> Tuple[str, Dict[str, Any]]:
        """自定义API调用实现"""
        import httpx

        async with httpx.AsyncClient() as client:
            # 根据具体API格式调整请求结构
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

            # 解析响应（需要根据具体API格式调整）
            result = response.json()
            return result["content"], result.get("metadata", {})

    def get_supported_models(self) -> List[str]:
        return self.supported_models