# encoding: utf-8

from typing import Dict, List, Any
from dataclasses import dataclass, field
from attacker.base import BaseAttacker, BaseAttackerConfig
from model.interface import ModelInterface
from model.silicon_flow_api import SiliconFlowLLMConfig
from model.base import BaseLLMConfig, LLMGenerateConfig
from utils import is_user_turn,setup_logger
from configs import PAST_TENSE_TEMPLATE

logger = setup_logger(__name__)

@dataclass
class PastTenseAttackerConfig(BaseAttackerConfig):
    """
    Configuration for the Rewrite Attacker.

    :param attacker_cls: Class of the attacker, default is "PastTenseAttacker".
    :param attacker_name: Name of the attacker.  
    :param llm_config: Configuration for the language model.  
    :param llm_gen_config: Configuration for generating output with LLM.  
    :param rewrite_template: Template for rewriting user prompts.  
    """
    attacker_cls: str = field(default="PastTenseAttacker")
    attacker_name: str = field(default=None)
    attack_type: any = field(default=None)
    llm_config: BaseLLMConfig = field(default_factory=SiliconFlowLLMConfig)
    llm_gen_config: LLMGenerateConfig = field(default=LLMGenerateConfig)
    rewrite_template: str = field(default=PAST_TENSE_TEMPLATE)



class PastTenseAttacker(BaseAttacker):
    """
    PastTense Attacker Implementation for modifying user prompts to bypass restrictions.

    :param config: Configuration for the PastTense Attacker.
    """

    def __init__(self, config: PastTenseAttackerConfig):
        super().__init__(config)
        self.llm = ModelInterface().create_llm(config=config.llm_config)
        self.llm_gen_config = config.llm_gen_config
        self.rewrite_template = config.rewrite_template

    def reform_template(self, prompt: str) -> str:
        """
        Rewrite the given prompt using the specified template.

        :param prompt: The original user prompt. 
        :return: The rewritten prompt.  
        """
        reformat_content =self.rewrite_template.format(content=prompt)
        logger.debug(f"Get formatted past tense message:{reformat_content}")

        messages = [{
            "role": "user",
            "content": reformat_content,
        }]
        jailbreak_content = self.llm.generate(messages,self.llm_gen_config)[-1]["content"]
        logger.debug(f"Get jailbreak output:{jailbreak_content}")

        return jailbreak_content

    def attack(
            self,
            messages: List[Dict[str, str]],
            **kwargs
    ) -> List[Dict[str, str]]:
        """
        Execute an attack by rewriting the latest user prompt.

        :param messages: List of messages in the conversation.  
        :param kwargs: Additional parameters for the attack.
        :return: Modified list of messages with the rewritten prompt.  
        """
        logger.debug(f"The input messages of past tense attack is:{messages}")
        assert is_user_turn(messages)

        jailbreak_content = self.reform_template(messages[-1]["content"])
        messages[-1]["content"] = jailbreak_content

        logger.debug(f"The output messages of rewrite attack is:{messages}")
        logger.info(f"Get final messages from rewrite attack!!")

        return messages
