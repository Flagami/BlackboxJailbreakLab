from typing import Dict, List, Any, Optional, Tuple, Generator
from dataclasses import dataclass, field
import logging
from model.base import BaseLLMConfig, LLMGenerateConfig, BaseLLM
from utils import setup_logger
from configs import ModelConfig

logger = setup_logger(__name__)


@dataclass
class OpenAILLMConfig(BaseLLMConfig):
    llm_type: str = field(default="openai_compatible")
    model_name: str = field(default=None)
    base_url: str = field(default=None)
    api_key: str = field(default=None)

    def __post_init__(self):
        cfg = ModelConfig()
        if self.model_name is None:
            self.model_name = cfg.model_name
        if self.base_url is None:
            self.base_url = cfg.api_base
        if self.api_key is None:
            self.api_key = cfg.api_key


class OpenAIInterface(BaseLLM):
    """OpenAI-compatible async API interface"""

    def __init__(self, config: OpenAILLMConfig):
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = config.base_url

    async def call_model(self,
                         messages: List[Dict[str, str]],
                         model_name: str,
                         **kwargs) -> Tuple[str, Dict[str, Any]]:
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
        return []

    def generate(self, messages, config=None):
        raise NotImplementedError("Use call_model for async calls.")

    def continual_generate(self, messages, config):
        raise NotImplementedError

    def evaluate_log_likelihood(self, messages, config):
        raise NotImplementedError