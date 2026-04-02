from enum import Enum
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from configs import MAX_CONVERSATION_TURNS

# ============= 数据模型定义 =============

class AttackType(Enum):
    """攻击类型枚举 TODO:Add more attack type base on the demand"""
    JAILBREAK = "black_box"  # 越狱攻击
    PROMPT_INJECTION = "black_box"  # 提示注入
    ADVERSARIAL = "black_box"  # 对抗性攻击
    SOCIAL_ENGINEERING = "black_box"  # 社会工程学
    ROLEPLAY = "black_box"  # 角色扮演
    MULTI_TURN = "black_box"  # 多轮对话攻击
    OVERLOAD="black_box"
    ICA="black_box"
    REWRITE="black_box"
    PAST_TENSE="black_box"
    RENE_LLM="black_box"
    ART_PROMPT="black_box"
    DEEP_INCEPTION="black_box"
    GPT4_CIPHER="black_box"
    RANDOM_SEARCH="black_box"
    TAP="black_box"  # 白盒攻击
    PAIR = "black_box" # 白盒攻击

class AttackResult(Enum):
    """攻击结果枚举"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    ERROR = "error"

@dataclass
class ConversationTurn:
    """单轮对话记录"""
    role: str  # user/assistant
    content: str
    turn_number: int
    timestamp: datetime
    token_count: Optional[int] = None

@dataclass
class AttackRequest:
    """攻击请求参数"""
    attack_method: str  # 攻击手段名称
    attack_model: str   # 攻击模型名称
    target_model: str   # 被攻击模型名称
    attack_payload: Optional[str] = None  # 自定义攻击载荷
    max_turns: int = MAX_CONVERSATION_TURNS  # 最大对话轮数
    temperature: float = 0.7
    custom_params: Dict[str, Any] = None

@dataclass
class AttackResponse:
    """攻击响应结果"""
    request_id: str
    attack_method: str
    attack_model: str
    target_model: str
    conversation_history_target_model: List[ConversationTurn]
    conversation_history_attacker_model: List[ConversationTurn]
    attack_result: AttackResult
    success_probability: float  # 攻破概率 0-1
    vulnerability_score: float  # 漏洞分数 0-100
    execution_time: float  # 执行时间（秒）
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
