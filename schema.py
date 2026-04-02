from enum import Enum
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from configs import MAX_CONVERSATION_TURNS

# ============= Data Model Definitions =============

class AttackType(Enum):
    """Attack type enumeration"""
    JAILBREAK = "black_box"  # Jailbreak attack
    PROMPT_INJECTION = "black_box"  # Prompt injection
    ADVERSARIAL = "black_box"  # Adversarial attack
    SOCIAL_ENGINEERING = "black_box"  # Social engineering
    ROLEPLAY = "black_box"  # Role play
    MULTI_TURN = "black_box"  # Multi-turn conversation attack
    OVERLOAD="black_box"
    ICA="black_box"
    REWRITE="black_box"
    PAST_TENSE="black_box"
    RENE_LLM="black_box"
    ART_PROMPT="black_box"
    DEEP_INCEPTION="black_box"
    GPT4_CIPHER="black_box"
    RANDOM_SEARCH="black_box"
    TAP="black_box"  # White-box attack
    PAIR = "black_box" # White-box attack

class AttackResult(Enum):
    """Attack result enumeration"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    ERROR = "error"

@dataclass
class ConversationTurn:
    """Single conversation turn record"""
    role: str  # user/assistant
    content: str
    turn_number: int
    timestamp: datetime
    token_count: Optional[int] = None

@dataclass
class AttackRequest:
    """Attack request parameters"""
    attack_method: str  # Attack method name
    attack_model: str   # Attack model name
    target_model: str   # Target model name
    attack_payload: Optional[str] = None  # Custom attack payload
    max_turns: int = MAX_CONVERSATION_TURNS  # Max conversation turns
    temperature: float = 0.7
    custom_params: Dict[str, Any] = None

@dataclass
class AttackResponse:
    """Attack response result"""
    request_id: str
    attack_method: str
    attack_model: str
    target_model: str
    conversation_history_target_model: List[ConversationTurn]
    conversation_history_attacker_model: List[ConversationTurn]
    attack_result: AttackResult
    success_probability: float  # Success probability 0-1
    vulnerability_score: float  # Vulnerability score 0-100
    execution_time: float  # Execution time (seconds)
    metadata: Dict[str, Any]

if __name__ == '__main__':
    conversation_history = []
    turn = 0
    for i in range(MAX_CONVERSATION_TURNS):
        conversation_history.append(ConversationTurn(
            role="user",
            content="hello",
            turn_number=turn + 1,
            timestamp=datetime.now(),
        ))


        conversation_history.append(ConversationTurn(
            role="assistant",
            content="hi there",
            turn_number=turn + 1,
            timestamp=datetime.now(),
        ))

    print(f"{type(conversation_history)}:\n{conversation_history}")
