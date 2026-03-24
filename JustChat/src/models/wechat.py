"""
微信数据模型模块
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WeChatMessage:
    """微信消息数据类"""
    message_id: str
    from_user: str
    to_user: str
    content: str
    message_type: str  # text, image, etc.
    timestamp: datetime

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'message_id': self.message_id,
            'from_user': self.from_user,
            'to_user': self.to_user,
            'content': self.content,
            'message_type': self.message_type,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class WeChatConfig:
    """微信配置数据类"""
    avatar_path: Optional[str] = None
    nickname: Optional[str] = None
    signature: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'avatar_path': self.avatar_path,
            'nickname': self.nickname,
            'signature': self.signature
        }
