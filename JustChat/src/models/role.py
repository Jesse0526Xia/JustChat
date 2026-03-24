"""
角色数据模型模块
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import json


@dataclass
class RoleModel:
    """角色数据模型"""
    character_id: str
    name: str
    age: int
    occupation: str
    background: str
    personality_traits: List[str]
    avatar_path: Optional[str] = None
    speaking_style: str = 'CASUAL'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row: tuple) -> 'RoleModel':
        """
        从数据库行创建角色模型

        Args:
            row: 数据库行元组

        Returns:
            角色模型实例
        """
        return cls(
            character_id=row[0],
            name=row[1],
            age=row[2],
            occupation=row[3],
            background=row[4],
            personality_traits=json.loads(row[5]) if row[5] else [],
            avatar_path=row[6],
            speaking_style=row[7],
            created_at=datetime.fromisoformat(row[8]) if row[8] else None,
            updated_at=datetime.fromisoformat(row[9]) if row[9] else None
        )

    def to_db_tuple(self) -> tuple:
        """
        将角色模型转换为数据库元组

        Returns:
            数据库元组
        """
        return (
            self.character_id,
            self.name,
            self.age,
            self.occupation,
            self.background,
            json.dumps(self.personality_traits, ensure_ascii=False),
            self.avatar_path,
            self.speaking_style,
            self.created_at.isoformat() if self.created_at else None,
            self.updated_at.isoformat() if self.updated_at else None
        )

    def to_dict(self) -> dict:
        """
        将角色模型转换为字典

        Returns:
            角色字典
        """
        return {
            'character_id': self.character_id,
            'name': self.name,
            'age': self.age,
            'occupation': self.occupation,
            'background': self.background,
            'personality_traits': self.personality_traits,
            'avatar_path': self.avatar_path,
            'speaking_style': self.speaking_style,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
