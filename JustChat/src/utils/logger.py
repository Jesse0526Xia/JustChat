"""
日志管理器模块
提供统一的日志记录功能
"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


class LogManager:
    """日志管理器类，提供统一的日志记录功能"""

    _instance: Optional['LogManager'] = None

    def __new__(cls, log_dir: str = 'logs', log_level: str = 'INFO'):
        """单例模式确保全局只有一个日志实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_dir: str = 'logs', log_level: str = 'INFO'):
        """
        初始化日志管理器

        Args:
            log_dir: 日志目录路径
            log_level: 日志级别 (INFO, WARNING, ERROR)
        """
        if self._initialized:
            return

        self.log_dir = Path(log_dir)
        self.log_level = getattr(logging, log_level.upper())
        self.logger = None

        # 创建日志目录
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 初始化日志系统
        self._setup_logger()

        self._initialized = True

    def _setup_logger(self):
        """设置日志处理器"""
        self.logger = logging.getLogger('virtual_lover')
        self.logger.setLevel(self.log_level)

        # 清除现有的处理器
        self.logger.handlers.clear()

        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 文件处理器（自动轮转）
        log_file = self.log_dir / 'virtual_lover.log'
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """记录INFO级别日志"""
        if self.logger:
            self.logger.info(message)

    def warning(self, message: str):
        """记录WARNING级别日志"""
        if self.logger:
            self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """
        记录ERROR级别日志

        Args:
            message: 错误消息
            exc_info: 是否包含异常堆栈信息
        """
        if self.logger:
            self.logger.error(message, exc_info=exc_info)

    def debug(self, message: str):
        """记录DEBUG级别日志"""
        if self.logger:
            self.logger.debug(message)

    def critical(self, message: str):
        """记录CRITICAL级别日志"""
        if self.logger:
            self.logger.critical(message)
