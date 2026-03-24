"""
数据库管理器模块
提供数据库连接和初始化功能
"""

import sqlite3
import shutil
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple, Any


class DatabaseManager:
    """数据库管理器类，提供数据库连接和初始化功能"""

    def __init__(self, db_path: str = 'data/virtual_lover.db'):
        """
        初始化数据库管理器

        Args:
            db_path: 数据库文件路径
        """
        self.db_path = Path(db_path)
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self):
        """建立数据库连接"""
        # 确保数据目录存在
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # 建立连接
        self.connection = sqlite3.connect(str(self.db_path))
        # 启用外键约束
        self.connection.execute("PRAGMA foreign_keys = ON")

    def disconnect(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None

    @contextmanager
    def get_cursor(self):
        """
        获取数据库游标的上下文管理器

        Yields:
            数据库游标
        """
        if not self.connection:
            raise RuntimeError("数据库未连接，请先调用connect()方法")

        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def initialize_tables(self):
        """初始化所有数据表"""
        with self.get_cursor() as cursor:
            # 创建角色表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS roles (
                    character_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    occupation TEXT,
                    background TEXT,
                    personality_traits TEXT,
                    avatar_path TEXT,
                    speaking_style TEXT DEFAULT 'CASUAL',
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')

            # 创建记忆表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    memory_id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    importance REAL DEFAULT 0.5,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (character_id) REFERENCES roles(character_id) ON DELETE CASCADE
                )
            ''')

            # 创建故事表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stories (
                    story_id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    file_id TEXT NOT NULL,
                    title TEXT,
                    content TEXT NOT NULL,
                    timestamp TEXT,
                    keywords TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (character_id) REFERENCES roles(character_id) ON DELETE CASCADE,
                    FOREIGN KEY (file_id) REFERENCES story_files(file_id) ON DELETE CASCADE
                )
            ''')

            # 创建故事文件表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS story_files (
                    file_id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    uploaded_at TEXT NOT NULL,
                    event_count INTEGER DEFAULT 0,
                    FOREIGN KEY (character_id) REFERENCES roles(character_id) ON DELETE CASCADE
                )
            ''')

            # 创建配置表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configs (
                    config_id TEXT PRIMARY KEY,
                    config_key TEXT UNIQUE NOT NULL,
                    config_value TEXT NOT NULL,
                    description TEXT,
                    updated_at TEXT NOT NULL
                )
            ''')

            # 创建索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_memories_character_id
                ON memories(character_id)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_memories_created_at
                ON memories(created_at)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_stories_character_id
                ON stories(character_id)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_story_files_character_id
                ON story_files(character_id)
            ''')

            # 提交事务
            self.connection.commit()

    def execute(self, sql: str, params: Tuple = (), commit: bool = True) -> int:
        """
        执行SQL语句

        Args:
            sql: SQL语句
            params: 参数元组
            commit: 是否提交事务

        Returns:
            影响的行数
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            if commit:
                self.connection.commit()
            return cursor.rowcount

    def fetch_one(self, sql: str, params: Tuple = ()) -> Optional[Tuple]:
        """
        查询单条记录

        Args:
            sql: SQL语句
            params: 参数元组

        Returns:
            查询结果，如果没有则返回None
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def fetch_all(self, sql: str, params: Tuple = ()) -> List[Tuple]:
        """
        查询多条记录

        Args:
            sql: SQL语句
            params: 参数元组

        Returns:
            查询结果列表
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def backup(self, backup_dir: str = 'backup') -> str:
        """
        备份数据库

        Args:
            backup_dir: 备份目录路径

        Returns:
            备份文件路径
        """
        if not self.connection:
            raise RuntimeError("数据库未连接，请先调用connect()方法")

        # 确保备份目录存在
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        # 生成备份文件名（包含时间戳）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_path / f'virtual_lover_{timestamp}.db'

        # 复制数据库文件
        shutil.copy2(str(self.db_path), str(backup_file))

        return str(backup_file)

    def restore(self, backup_file: str):
        """
        从备份文件恢复数据库

        Args:
            backup_file: 备份文件路径
        """
        # 关闭当前连接
        self.disconnect()

        # 恢复备份文件
        shutil.copy2(backup_file, str(self.db_path))

        # 重新建立连接
        self.connect()

    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()
