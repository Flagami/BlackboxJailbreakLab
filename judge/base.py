
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from schema import ConversationTurn,AttackType,AttackResult
from utils import setup_logger

logger = setup_logger()

class ResultJudge(ABC):

    @abstractmethod
    async def judge_attack_result(self, 
                                conversation_history: List[ConversationTurn],
                                attack_type: AttackType) -> Tuple[AttackResult, float, float]:

        pass



@dataclass
class BaseJudgeConfig(ABC):
    """
    Base configuration for the Judge class.

    :param judge_cls: Class of the judge, default is None.
    :param judge_name: Name of the judge, default is None.
    """
    judge_cls: str = field(default=None)
    judge_name: str = field(default=None)


class BaseJudge(ABC):
    """
    Base class for implementing a judge to evaluate the safety of a given response.

    :param config: Configuration for the judge.
    """

    def __init__(
            self,
            config: BaseJudgeConfig,
    ):
        self._CLS = config.judge_cls
        self._NAME = config.judge_name

    @abstractmethod
    def judge(
            self,
            messages: List[Dict[str, str]] = None,
            request: str = None
    ) -> int:
        """
        Abstract method to evaluate the safety of a given request and messages.

        :param messages: List of messages to evaluate.
        :param request: The user's request.
        :return: An integer representing the evaluation result (0: Unsafe, 1: Safe).
        """
        pass
