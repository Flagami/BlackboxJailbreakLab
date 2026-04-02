from abc import ABC, abstractmethod
from symtable import Class
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
# 自定义库
from schema import AttackType
from utils import setup_logger

logger = setup_logger(__name__)
# ============= 攻击策略配置 =============

@dataclass
class BaseAttackerConfig:
    """攻击器配置基类"""
    attacker_cls: str
    attacker_name: str
    attack_type: any

    max_retries: int = 3
    timeout: float = 30.0
    custom_params: Dict[str, Any] = None

    def __post_init__(self):
        if self.custom_params is None:
            self.custom_params = {}


# ============= 攻击策略接口 =============

class BaseAttacker(ABC):
    """
    Abstract Base Class for Attacker.

    :param config: Configuration for the attacker.
    """

    def __init__(self, config: BaseAttackerConfig):
        self._CLS = config.attacker_cls
        self._NAME = config.attacker_name
        self._TYPE = config.attack_type
        self._config = config

    @abstractmethod
    def attack(
            self,
            messages: List[Dict[str, str]],
            **kwargs
    ) -> List[Dict[str, str]]:
        """
        Abstract method to execute an attack on a sequence of messages.

        :param messages: List of input messages.
        :param kwargs: Additional parameters for the attack.
        :return: Modified list of messages after the attack.
        """
        if messages is None:
            messages = []
        else:
            assert messages[-1]["role"] != "assistant"
        pass

    def get_attack_type(self) -> AttackType:
        """获取攻击类型"""
        return self._TYPE

    def get_attacker_name(self) -> str:
        """获取攻击器名称"""
        return self._NAME

    def get_attacker_cls(self) -> str:
        """获取攻击器类名"""
        return self._CLS

