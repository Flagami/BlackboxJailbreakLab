# encoding: utf-8
"""gpt4_cipher: https://arxiv.org/abs/2308.06463 ICLR 2024
https://github.com/RobustNLP/CipherChat
"""
from distutils.command.config import config
from typing import Dict, List, Any
from dataclasses import dataclass, field
from attacker.base import BaseAttacker, BaseAttackerConfig
from configs import ASCII_CIPHER_TEMPLATE
from utils import setup_logger,is_user_turn

logger = setup_logger(__name__)

@dataclass
class GPT4CipherAttackerConfig(BaseAttackerConfig):
    """
    Configuration for the GPT4Cipher Attacker.

    :param attacker_cls: Class of the attacker, default is "GPT4CipherAttacker".
    :param attacker_name: Name of the attacker.
    :param rewrite_template: Template for LLM to do GPT4Cipher attack
    """

    attacker_cls: str = field(default="GPT4CipherAttacker")
    attacker_name: str = field(default="GPT4Cipher")
    attack_type: any = field(default=None)
    shift_number: int = field(default=2)
    rewrite_template: str = field(default=ASCII_CIPHER_TEMPLATE)



class GPT4CipherAttacker(BaseAttacker):
    """
    GPT4Cipher Attacker Implementation for modifying user prompts to bypass restrictions.
    """

    def __init__(self, config: GPT4CipherAttackerConfig):
        super().__init__(config)

        self.rewrite_template = config.rewrite_template
        self.shift_number = config.shift_number


    def caesar_cipher(self, text, shift=3)-> str:
        """
        To transfer a string into Caesar Cipher
        :param text: string waiting to be transferred
        :param shift: shift digits in Caesar Cipher
        """

        result = []


        for char in text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                shifted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
                result.append(shifted_char)
            else:
                result.append(char)
        logger.debug(f"Get caesar cipher result: {result}")
        logger.info(f"Get caesar cipher result with length: {len(result)}")
        return ''.join(result)

    def reform_prompt(self,caesar_cipher):
        reform_template = self.rewrite_template.replace(">>shit_num<<", str(self.shift_number))
        return reform_template + caesar_cipher

    def attack(
            self,
            messages: List[Dict[str, str]],
            **kwargs
    ) -> List[Dict[str, str]]:
        """
        Execute an attack by transfer the latest user prompt to GPT4Cipher.

        :param messages: List of messages in the conversation.  
        :param kwargs: Additional parameters for the attack.  
        :return: Modified list of messages with the rewritten prompt.  
        """
        logger.debug(f"The input messages of rewrite attack is:{messages}")

        assert is_user_turn(messages)

        original_prompt = messages[-1]["content"]

        # TODO：适配更多的cipher手段 unicode\gbk\utf\atbash\morse\unchange
        caesar_cipher = self.caesar_cipher(text=original_prompt, shift=self.shift_number)

        messages[-1]["content"] = self.reform_prompt(caesar_cipher=caesar_cipher)

        logger.debug(f"The output messages of gpt4 cipher attack is:{messages}")
        logger.info(f"Get final messages from gpt4 cipher attack!!")
        return messages



