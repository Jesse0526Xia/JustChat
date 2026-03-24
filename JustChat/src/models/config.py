"""
配置数据模型模块
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SystemConfig:
    """系统配置数据模型"""
    # 数据库配置
    database_path: str = 'data/virtual_lover.db'

    # 日志配置
    log_level: str = 'INFO'
    log_dir: str = 'logs'

    # 缓存配置
    cache_ttl: int = 3600

    # 备份配置
    backup_enabled: bool = True
    backup_dir: str = 'backup'
    backup_keep_days: int = 30

    # 微信配置
    wechat_auto_reconnect: bool = True
    wechat_max_attempts: int = 3

    # 对话配置
    dialogue_model: str = 'gpt-3.5-turbo'
    dialogue_max_tokens: int = 1000
    dialogue_temperature: float = 0.7

    # OpenAI配置
    openai_api_key: str = ''

    # 加密配置
    encryption_key: str = ''

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'database_path': self.database_path,
            'log_level': self.log_level,
            'log_dir': self.log_dir,
            'cache_ttl': self.cache_ttl,
            'backup_enabled': self.backup_enabled,
            'backup_dir': self.backup_dir,
            'backup_keep_days': self.backup_keep_days,
            'wechat_auto_reconnect': self.wechat_auto_reconnect,
            'wechat_max_attempts': self.wechat_max_attempts,
            'dialogue_model': self.dialogue_model,
            'dialogue_max_tokens': self.dialogue_max_tokens,
            'dialogue_temperature': self.dialogue_temperature,
            'openai_api_key': self.openai_api_key,
            'encryption_key': self.encryption_key
        }
