"""
角色档案数据模型模块
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class PersonalityTrait(str, Enum):
    """性格特征枚举"""
    GENTLE = "gentle"  # 温柔
    ACTIVE = "active"  # 活泼
    INTROVERTED = "introverted"  # 内向
    HUMOROUS = "humorous"  # 幽默
    SERIOUS = "serious"  # 严肃


class SpeakingStyle(str, Enum):
    """说话风格枚举"""
    FORMAL = "formal"  # 正式
    CUTE = "cute"  # 可爱
    CASUAL = "casual"  # 随意
    ROMANTIC = "romantic"  # 浪漫


@dataclass
class CharacterProfile:
    """角色档案数据类"""
    character_id: str
    name: str
    age: int
    occupation: str
    background: str
    personality_traits: List[PersonalityTrait]
    avatar_path: Optional[str] = None
    speaking_style: SpeakingStyle = SpeakingStyle.CASUAL
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'character_id': self.character_id,
            'name': self.name,
            'age': self.age,
            'occupation': self.occupation,
            'background': self.background,
            'personality_traits': [trait.value for trait in self.personality_traits],
            'avatar_path': self.avatar_path,
            'speaking_style': self.speaking_style.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
