from typing import Dict, List, Any, Optional, Tuple,Generator
from dataclasses import dataclass, field
import logging
# 自定义库
from model.base import BaseLLMConfig,LLMGenerateConfig,BaseLLM
from utils import setup_logger
from configs import SILICON_FLOW_SUPPORTED_MODELS,ModelConfig

logger = setup_logger(__name__)


@dataclass
class OpenAILLMConfig(BaseLLMConfig):
    """
    SiliconFlow Chat LLM Configuration.

    :param llm_type: Type of LLM, default is "SiliconFlowLLM".
    :param model_name: Name of the model.
    :param base_url: Base URL for the OpenAI API.
    :param api_key: API key for accessing OpenAI.
    """

    llm_type: str = field(default="SiliconFlowLLM")
    model_name: str = field(default="THUDM/GLM-4-9B-0414")
    base_url: str = field(default=ModelConfig().silicon_flow_api_base)
    api_key: str = field(default=ModelConfig().silicon_flow_api_key)

class OpenAIInterface(BaseLLM):
    """OpenAI API接口实现"""

    def __init__(self, config:OpenAILLMConfig):
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = config.base_url
        self.supported_models = ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]

    async def call_model(self,
                         messages: List[Dict[str, str]],
                         model_name: str,
                         **kwargs) -> Tuple[str, Dict[str, Any]]:
        """OpenAI API调用实现"""
        # 实际实现中需要使用openai库或httpx发送请求
        # 这里提供接口框架
        import openai

        client = openai.AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

        try:
            response = await client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 2048)
            )

            content = response.choices[0].message.content
            metadata = {
                "usage": dict(response.usage),
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason
            }

            return content, metadata
        except Exception as e:
            logging.error(f"OpenAI API Failed: {e}")
            raise

    def get_supported_models(self) -> List[str]:
        return self.supported_models