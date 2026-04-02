
from abc import ABC
from typing import Type, Dict, List
from model import BaseLLMConfig
from model.base import BaseLLM
from model.silicon_flow_api import SiliconFlowLLM
from utils import setup_logger


logger = setup_logger(__name__)


class ModelInterface(ABC):
    """模型调用抽象接口"""

    _registry: Dict[str, Type['BaseLLM']] = {"silicon_flow": SiliconFlowLLM}

    @classmethod
    def register(cls, llm_type: str, llm_cls: Type['BaseLLM']):
        cls._registry[llm_type] = llm_cls

    def create_llm(self, config: 'BaseLLMConfig') -> 'BaseLLM':
        llm_type = config.llm_type
        if llm_type not in self._registry:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
        logger.info(f"LLM type: {llm_type} registered successfully")
        return self._registry[llm_type](config)

    def get_supported_models(self) -> List[str]:
        return list(self._registry.keys())

