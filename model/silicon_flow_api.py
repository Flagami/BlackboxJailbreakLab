from typing import Dict, List, Any, Optional, Tuple, Generator
from dataclasses import dataclass, field
import openai
import time
from model.base import BaseLLM, BaseLLMConfig, LLMGenerateConfig
from utils import setup_logger
from configs import ModelConfig

logger = setup_logger(__name__)


@dataclass
class SiliconFlowLLMConfig(BaseLLMConfig):
    """OpenAI-compatible LLM configuration.

    Reads api_key and base_url from the unified ModelConfig (OPENAI_API_KEY /
    OPENAI_BASE_URL env vars), so any OpenAI-compatible provider works out of
    the box — including SiliconFlow, Together AI, Groq, local vLLM, etc.
    """

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


@dataclass
class SiliconFlowLLMGenerateConfig:
    max_n_tokens: int = field(default=None)
    temperature: float = field(default=None)
    logprobs: bool = field(default=False)
    seed: int = field(default=None)
    stream: bool = field(default=False)


class SiliconFlowLLM(BaseLLM):
    """OpenAI-compatible API interface (works with SiliconFlow, OpenAI, etc.)"""

    def __init__(self, config: SiliconFlowLLMConfig):
        super().__init__(config)
        self.client = openai.OpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
        )

    def get_supported_models(self) -> List[str]:
        return []

    def generate(
            self,
            messages: List[Dict[str, str]],
            config: SiliconFlowLLMGenerateConfig = SiliconFlowLLMGenerateConfig,
    ) -> list[dict[str, str]] | tuple[list[dict[str, str]], list[Any]] | Generator[str, None, None] | None:
        model_name = self._NAME
        retry_count = 1
        max_retries = 3
        logger.debug(f"Check the generate messages:{messages}")

        while retry_count < max_retries:
            logger.info(f"Start calling {model_name} for {retry_count}/{max_retries} time....")
            try:
                if config.stream:
                    full_content = ""
                    prompt_tokens = 0
                    completion_tokens = 0

                    stream = self.client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=config.max_n_tokens,
                        temperature=config.temperature,
                        seed=config.seed,
                        stream=True,
                    )

                    def stream_response():
                        nonlocal full_content, prompt_tokens, completion_tokens
                        for chunk in stream:
                            if chunk.choices and chunk.choices[0].delta.content:
                                content_piece = chunk.choices[0].delta.content
                                full_content += content_piece
                                yield content_piece
                            if hasattr(chunk, 'usage') and chunk.usage:
                                if hasattr(chunk.usage, 'prompt_tokens'):
                                    prompt_tokens = chunk.usage.prompt_tokens
                                if hasattr(chunk.usage, 'completion_tokens'):
                                    completion_tokens = chunk.usage.completion_tokens

                    response_generator = stream_response()

                    def wrapped_generator():
                        yield from response_generator
                        messages.append({"role": "assistant", "content": full_content})

                    logger.info("Get streaming response successfully!")
                    return wrapped_generator()

                else:
                    response = self.client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        temperature=config.temperature,
                        logprobs=config.logprobs,
                        seed=config.seed,
                    )

                    if response.choices is None:
                        logger.error("Cannot find choices in Response: %s", response)
                        messages.append({"role": "assistant", "content": "I'm sorry, but I can't fulfill this request."})
                    else:
                        content = response.choices[0].message.content
                        messages.append({"role": "assistant", "content": content})

                    if config.logprobs:
                        logs = [c.logprob for c in response.choices[0].logprobs.content]
                        return messages, logs

                    logger.info(f"Response received on attempt {retry_count}/{max_retries}")
                    return messages

            except Exception as e:
                if "安全" in str(e) or "敏感" in str(e) or "safety" in str(e).lower() or "sensitive" in str(e).lower():
                    messages.append({"role": "assistant", "content": "I'm sorry, I can't help with that."})
                    logger.error(f"Safety error from model {model_name}: {e}")
                    return messages

                retry_count += 1
                if retry_count >= max_retries:
                    messages.append({"role": "assistant", "content": "I'm sorry, but I can't fulfill this request."})
                    logger.error(f"Max retries reached for model {model_name}: {e}")
                    exit(0)
                else:
                    logger.error(f"Retry {retry_count}/{max_retries} for model {model_name}: {e}")
                    time.sleep(retry_count)
        return messages

    def continual_generate(self, messages: List[Dict[str, str]], config: LLMGenerateConfig):
        raise NotImplementedError(
            "SiliconFlowLLM does not support continual generation."
        )

    def evaluate_log_likelihood(self, messages: List[Dict[str, str]], config: LLMGenerateConfig) -> List[float]:
        raise NotImplementedError(
            "SiliconFlowLLM does not support log likelihood evaluation."
        )
