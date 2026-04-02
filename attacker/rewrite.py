# encoding: utf-8
from typing import Dict, List, Any
from dataclasses import dataclass, field
from attacker.base import BaseAttacker, BaseAttackerConfig
from model.base import BaseLLMConfig, LLMGenerateConfig
from model.silicon_flow_api import SiliconFlowLLMConfig
from model.interface import ModelInterface
from utils import is_user_turn,setup_logger
from configs import REWRITE_TEMPLATE

logger = setup_logger(__name__)

@dataclass
class RewriteAttackerConfig(BaseAttackerConfig):
    """
    Configuration for the Rewrite Attacker.

    :param attacker_cls: Class of the attacker, default is "RewriteAttacker".  
    :param attacker_name: Name of the attacker.  
    :param llm_config: Configuration for the language model.  
    :param llm_gen_config: Configuration for generating output with LLM.  
    :param rewrite_template: Template for rewriting user prompts.  
    """
    attacker_cls: str = field(default="RewriteAttacker")
    attacker_name: str = field(default=None)
    attack_type: any = field(default=None)
    llm_config: BaseLLMConfig = field(default_factory=SiliconFlowLLMConfig)
    llm_gen_config: LLMGenerateConfig = field(default=LLMGenerateConfig)
    rewrite_template: str = field(default=REWRITE_TEMPLATE)


class RewriteAttacker(BaseAttacker):
    """
    Rewrite Attacker Implementation for modifying user prompts to bypass restrictions.

    :param config: Configuration for the Rewrite Attacker.  
    """

    def __init__(self, config: RewriteAttackerConfig):
        super().__init__(config)
        self.llm = ModelInterface().create_llm(config=config.llm_config)
        self.llm_gen_config = config.llm_gen_config
        self.rewrite_template = config.rewrite_template
        # logger.debug(f"Check the rewrite info:\nllm:{self.llm}\nllm gen config:{self.llm_gen_config}\nrewrite template:{self.rewrite_template}")

    def rewrite(self, prompt: str) -> str:
        """
        Rewrite the given prompt using the specified template.

        :param prompt: The original user prompt. 
        :return: The rewritten prompt.  
        """
        rewritten_content = self.rewrite_template.format(content=prompt)
        logger.debug(f"Get formatted rewritten message:{rewritten_content}")

        messages = [{
            "role": "user",
            "content": rewritten_content,
        }]
        logger.info(f"Start to request llm to jailbreak rewrite output...")
        jailbreak_content = self.llm.generate(messages,self.llm_gen_config,)[-1]["content"]
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
        logger.debug(f"The input messages of rewrite attack is:{messages}")
        assert is_user_turn(messages)

        jailbreak_content = self.rewrite(messages[-1]["content"])
        messages[-1]["content"] = jailbreak_content

        logger.debug(f"The output messages of rewrite attack is:{messages}")
        logger.info(f"Get final messages from rewrite attack!!")

        return messages
