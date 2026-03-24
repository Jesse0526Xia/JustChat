"""
记忆数据模型模块
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
import json


class MemoryType(str, Enum):
    """记忆类型枚举"""
    DIALOGUE = "dialogue"  # 对话记忆
    STORY = "story"  # 故事记忆
    CUSTOM = "custom"  # 自定义记忆


@dataclass
class Memory:
    """记忆数据类"""
    memory_id: str
    character_id: str
    memory_type: MemoryType
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    importance: float = 0.5

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'memory_id': self.memory_id,
            'character_id': self.character_id,
            'memory_type': self.memory_type.value,
            'content': self.content,
            'metadata': self.metadata,
            'importance': self.importance,
            'created_at': self.created_at.isoformat()
        }


class MemoryModel:
    """记忆数据模型（数据库）"""
    def __init__(self, memory_id: str, character_id: str, memory_type: str,
                 content: str, metadata: Dict[str, Any], importance: float, created_at: datetime):
        self.memory_id = memory_id
        self.character_id = character_id
        self.memory_type = memory_type
        self.content = content
        self.metadata = metadata
        self.importance = importance
        self.created_at = created_at

    @classmethod
    def from_db_row(cls, row: tuple) -> 'MemoryModel':
        """从数据库行创建记忆模型"""
        return cls(
            memory_id=row[0],
            character_id=row[1],
            memory_type=row[2],
            content=row[3],
            metadata=json.loads(row[4]) if row[4] else {},
            importance=row[5] if row[5] is not None else 0.5,
            created_at=datetime.fromisoformat(row[6])
        )

    def to_memory(self) -> Memory:
        """转换为Memory对象"""
        return Memory(
            memory_id=self.memory_id,
            character_id=self.character_id,
            memory_type=MemoryType(self.memory_type),
            content=self.content,
            metadata=self.metadata,
            created_at=self.created_at,
            importance=self.importance
        )
