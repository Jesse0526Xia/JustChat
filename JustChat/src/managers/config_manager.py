"""
配置管理器模块
提供配置文件的读写功能
"""

import configparser
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from src.models.config import SystemConfig
from src.utils.logger import LogManager


class ConfigManager:
    """配置管理器类，提供配置文件的读写功能"""

    def __init__(self, config_dir: str = 'config'):
        """
        初始化配置管理器

        Args:
            config_dir: 配置目录路径
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.config_dir / 'config.ini'
        self.env_file = self.config_dir / '.env'

        self.config = configparser.ConfigParser()
        self.logger = LogManager()

    def load_config(self) -> SystemConfig:
        """
        加载配置文件

        Returns:
            系统配置对象
        """
        # 加载环境变量
        self.load_env()

        # 加载配置文件
        if self.config_file.exists():
            self.config.read(str(self.config_file), encoding='utf-8')

        # 创建配置对象
        system_config = SystemConfig()

        # 从配置文件读取配置
        if self.config.has_section('database'):
            system_config.database_path = self.config.get('database', 'path', fallback='data/virtual_lover.db')

        if self.config.has_section('log'):
            system_config.log_level = self.config.get('log', 'level', fallback='INFO')
            system_config.log_dir = self.config.get('log', 'dir', fallback='logs')

        if self.config.has_section('cache'):
            system_config.cache_ttl = self.config.getint('cache', 'ttl', fallback=3600)

        if self.config.has_section('backup'):
            system_config.backup_enabled = self.config.getboolean('backup', 'enabled', fallback=True)
            system_config.backup_dir = self.config.get('backup', 'dir', fallback='backup')
            system_config.backup_keep_days = self.config.getint('backup', 'keep_days', fallback=30)

        if self.config.has_section('wechat'):
            system_config.wechat_auto_reconnect = self.config.getboolean('wechat', 'auto_reconnect', fallback=True)
            system_config.wechat_max_attempts = self.config.getint('wechat', 'max_attempts', fallback=3)

        if self.config.has_section('dialogue'):
            system_config.dialogue_model = self.config.get('dialogue', 'model', fallback='gpt-3.5-turbo')
            system_config.dialogue_max_tokens = self.config.getint('dialogue', 'max_tokens', fallback=1000)
            system_config.dialogue_temperature = self.config.getfloat('dialogue', 'temperature', fallback=0.7)

        # 从环境变量读取敏感配置
        system_config.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        system_config.encryption_key = os.getenv('ENCRYPTION_KEY', '')

        return system_config

    def save_config(self, config: SystemConfig):
        """
        保存配置文件

        Args:
            config: 系统配置对象
        """
        # 保存非敏感配置到config.ini
        if not self.config.has_section('database'):
            self.config.add_section('database')
        self.config.set('database', 'path', config.database_path)

        if not self.config.has_section('log'):
            self.config.add_section('log')
        self.config.set('log', 'level', config.log_level)
        self.config.set('log', 'dir', config.log_dir)

        if not self.config.has_section('cache'):
            self.config.add_section('cache')
        self.config.set('cache', 'ttl', str(config.cache_ttl))

        if not self.config.has_section('backup'):
            self.config.add_section('backup')
        self.config.set('backup', 'enabled', str(config.backup_enabled))
        self.config.set('backup', 'dir', config.backup_dir)
        self.config.set('backup', 'keep_days', str(config.backup_keep_days))

        if not self.config.has_section('wechat'):
            self.config.add_section('wechat')
        self.config.set('wechat', 'auto_reconnect', str(config.wechat_auto_reconnect))
        self.config.set('wechat', 'max_attempts', str(config.wechat_max_attempts))

        if not self.config.has_section('dialogue'):
            self.config.add_section('dialogue')
        self.config.set('dialogue', 'model', config.dialogue_model)
        self.config.set('dialogue', 'max_tokens', str(config.dialogue_max_tokens))
        self.config.set('dialogue', 'temperature', str(config.dialogue_temperature))

        # 写入文件
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)

        self.logger.info(f"配置已保存到 {self.config_file}")

    def get(self, section: str, key: str, fallback: Optional[str] = None) -> Optional[str]:
        """
        获取配置项

        Args:
            section: 配置节
            key: 配置键
            fallback: 默认值

        Returns:
            配置值
        """
        if self.config.has_section(section) and self.config.has_option(section, key):
            return self.config.get(section, key)
        return fallback

    def set(self, section: str, key: str, value: str):
        """
        设置配置项

        Args:
            section: 配置节
            key: 配置键
            value: 配置值
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)

        # 保存到文件
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def load_env(self):
        """加载环境变量文件"""
        if self.env_file.exists():
            load_dotenv(str(self.env_file))
            self.logger.info(f"环境变量已加载: {self.env_file}")
        else:
            self.logger.warning(f"环境变量文件不存在: {self.env_file}")

    def save_env(self, config: SystemConfig):
        """
        保存环境变量文件

        Args:
            config: 系统配置对象
        """
        with open(self.env_file, 'w', encoding='utf-8') as f:
            f.write(f"OPENAI_API_KEY={config.openai_api_key}\n")
            f.write(f"ENCRYPTION_KEY={config.encryption_key}\n")

        self.logger.info(f"环境变量已保存到 {self.env_file}")
