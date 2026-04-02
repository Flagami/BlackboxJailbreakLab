from typing import Dict, List, Any, Optional, Tuple,Generator
from dataclasses import dataclass, field
import openai
import time
# 自定义库
from model.base import BaseLLM
from model.base import BaseLLMConfig,LLMGenerateConfig,BaseLLM
from utils import setup_logger
from configs import SILICON_FLOW_SUPPORTED_MODELS,ModelConfig

logger = setup_logger(__name__)


@dataclass
class SiliconFlowLLMConfig(BaseLLMConfig):
    """
    SiliconFlow Chat LLM Configuration.

    :param llm_type: Type of LLM, default is "SiliconFlowLLM".
    :param model_name: Name of the model.
    :param base_url: Base URL for the OpenAI API.
    :param api_key: API key for accessing OpenAI.
    """

    llm_type: str = field(default="silicon_flow")
    model_name: str = field(default="THUDM/GLM-4-9B-0414")
    base_url: str = field(default=ModelConfig().silicon_flow_api_base)
    api_key: str = field(default=ModelConfig().silicon_flow_api_key)

@dataclass
class SiliconFlowLLMGenerateConfig:
    """
    Configuration for LLM generation.

    :param max_n_tokens: Maximum number of tokens to generate.
    :param temperature: Temperature for sampling randomness.
    :param logprobs: Whether to return log probabilities.
    :param seed: Seed for reproducibility.
    :param stream: Whether to use streaming generation.
    """

    max_n_tokens: int = field(default=None)
    temperature: float = field(default=None)
    logprobs: bool = field(default=False)
    seed: int = field(default=None)
    stream: bool = field(default=False)  # Default to non-streaming behavior

class SiliconFlowLLM(BaseLLM):
    """OpenAI API接口实现"""
    def __init__(self, config: SiliconFlowLLMConfig):
        super().__init__(config)

        self.client = openai.OpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
        )
        self.supported_models = SILICON_FLOW_SUPPORTED_MODELS

    def get_supported_models(self) -> List[str]:
        return self.supported_models

    def generate(
            self,
            messages: List[Dict[str, str]],
            config: SiliconFlowLLMGenerateConfig=SiliconFlowLLMGenerateConfig,
    ) -> list[dict[str, str]] | tuple[list[dict[str, str]], list[Any]] | Generator[str, None, None] | None:
        """
        Generate a response for a given input using OpenAI Chat API.

        :param messages: List of input messages.
        :param config: Configuration for LLM generation.
        :return: Generated response or response with logprobs or stream generator.
        """
        model_name = self._NAME
        retry_count = 1
        max_retries = 3
        logger.debug(f"Check the generate messages of silicon flow llm:{messages}")

        while retry_count < max_retries:
            logger.info(f"Start calling {model_name} for {retry_count}/{max_retries} time....")
            try:
                if config.stream:
                    logger.info(f"Start generating stream for {model_name}")
                    full_content = ""
                    prompt_tokens = 0
                    completion_tokens = 0

                    # Create a streaming request
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

                        # 更新使用统计
                        # self.update(
                        #     prompt_tokens or len(str(messages[:-1])) // 4,
                        #     completion_tokens or len(full_content) // 4,
                        #     1,
                        # )
                    logger.debug(f"Check final messages for streaming:\n {messages}")
                    logger.info(f"Get final messages for streaming response successfully!!")
                    return wrapped_generator()

                # Non-streaming mode (original code)
                else:
                    response = self.client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        temperature=config.temperature,
                        logprobs=config.logprobs,
                        seed=config.seed,
                    )

                    if response.choices is None:
                        logger.error("Cannot find choices in Response:", response)
                        messages.append({"role": "assistant", "content": "I'm sorry, but I can't fulfill this request."})

                    else:
                        content = response.choices[0].message.content
                        messages.append({"role": "assistant", "content": content})

                    if config.logprobs:
                        logs = [c.logprob for c in response.choices[0].logprobs.content]
                        return messages, logs
                    logger.debug(f"Check final messages for no-streaming:\n {messages}")
                    logger.info(f"Get final messages for no-streaming response successfully on {retry_count}/{max_retries} time!!")
                    return messages

            except Exception as e:
                if "安全" in str(e) or "敏感" in str(e):
                    messages.append({"role": "assistant", "content": "I'm sorry, I can't help with that."})
                    logger.error(f"API request Safety Issue model:{model_name}, Error: {e}, returning safety message.")
                    return messages

                retry_count += 1
                if retry_count >= max_retries:
                    messages.append({"role": "assistant", "content": "I'm sorry, but I can't fulfill this request."})
                    logger.error(
                        f"API request failed when testing model:{model_name}, tried: {max_retries}, Error: {e}")
                    exit(0)
                else:
                    logger.error(
                        f"API request failed when testing model:{model_name}，retrying {retry_count}/{max_retries}... Error: {e}")
                    time.sleep(retry_count)
        return messages

    def continual_generate(self, messages: List[Dict[str, str]], config: LLMGenerateConfig):
        """
        Remove EOS token in formatted prompt. Manually add generation prompt.

        :param messages: List of messages for input.
        :param config: Configuration for LLM generation.
        :raises NotImplementedError: OpenAiChatLLM does not support continual generation.
        """
        raise NotImplementedError(
            "SiliconFlowLLMConfig does not support continual generation, please use Other Model Interface instead."
        )

    def evaluate_log_likelihood(self, messages: List[Dict[str, str]], config: LLMGenerateConfig) -> List[float]:
        """
        Evaluate the log likelihood of the given messages.

        :param messages: List of messages for evaluation.
        :param config: Configuration for LLM generation.
        :raises NotImplementedError: OpenAI Chat does not support log likelihood evaluation.
        """
        raise NotImplementedError(
            "SiliconFlowLLMConfig Chat does not support log likelihood evaluation."
        )
