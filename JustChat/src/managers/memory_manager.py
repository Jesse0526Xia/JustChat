"""
记忆管理器模块
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from src.managers.database_manager import DatabaseManager
from src.models.memory import Memory, MemoryType, MemoryModel
from src.utils.logger import LogManager


class MemoryManager:
    """记忆管理器类"""

    def __init__(self, db_manager: DatabaseManager):
        """
        初始化记忆管理器

        Args:
            db_manager: 数据库管理器
        """
        self.db_manager = db_manager
        self.logger = LogManager()

    def add_memory(self, character_id: str, content: str,
                   memory_type: MemoryType = MemoryType.CUSTOM,
                   metadata: Optional[dict] = None,
                   importance: float = 0.5) -> str:
        """
        添加记忆

        Args:
            character_id: 角色ID
            content: 记忆内容
            memory_type: 记忆类型
            metadata: 元数据
            importance: 重要性

        Returns:
            记忆ID
        """
        memory_id = uuid.uuid4().hex
        created_at = datetime.now()

        if metadata is None:
            metadata = {}

        sql = '''
            INSERT INTO memories (memory_id, character_id, memory_type, content, metadata, importance, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        self.db_manager.execute(sql, (
            memory_id,
            character_id,
            memory_type.value,
            content,
            str(metadata),
            importance,
            created_at.isoformat()
        ))

        self.logger.info(f"记忆添加成功: {memory_id}")
        return memory_id

    def add_dialogue_memory(self, character_id: str, user_message: str,
                           bot_response: str) -> str:
        """
        添加对话记忆

        Args:
            character_id: 角色ID
            user_message: 用户消息
            bot_response: 机器人回复

        Returns:
            记忆ID
        """
        content = f"用户说: {user_message}\n我回复: {bot_response}"
        metadata = {
            "user_message": user_message,
            "bot_response": bot_response
        }
        return self.add_memory(character_id, content, MemoryType.DIALOGUE, metadata)

    def retrieve_relevant_memories(self, character_id: str, query: str,
                                   top_k: int = 5) -> List[Memory]:
        """
        检索相关记忆

        Args:
            character_id: 角色ID
            query: 查询内容
            top_k: 返回数量

        Returns:
            记忆列表
        """
        # 简单的关键词匹配
        sql = '''
            SELECT * FROM memories
            WHERE character_id = ? AND content LIKE ?
            ORDER BY importance DESC, created_at DESC
            LIMIT ?
        '''
        rows = self.db_manager.fetch_all(sql, (character_id, f"%{query}%", top_k))

        memories = []
        for row in rows:
            model = MemoryModel.from_db_row(row)
            memories.append(model.to_memory())

        return memories

    def get_recent_memories(self, character_id: str, limit: int = 10) -> List[Memory]:
        """
        获取最近的记忆

        Args:
            character_id: 角色ID
            limit: 返回数量

        Returns:
            记忆列表
        """
        sql = '''
            SELECT * FROM memories
            WHERE character_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        '''
        rows = self.db_manager.fetch_all(sql, (character_id, limit))

        memories = []
        for row in rows:
            model = MemoryModel.from_db_row(row)
            memories.append(model.to_memory())

        return memories

    def search_memories(self, character_id: str, keyword: str) -> List[Memory]:
        """
        搜索记忆

        Args:
            character_id: 角色ID
            keyword: 关键词

        Returns:
            记忆列表
        """
        sql = '''
            SELECT * FROM memories
            WHERE character_id = ? AND content LIKE ?
            ORDER BY created_at DESC
        '''
        rows = self.db_manager.fetch_all(sql, (character_id, f"%{keyword}%"))

        memories = []
        for row in rows:
            model = MemoryModel.from_db_row(row)
            memories.append(model.to_memory())

        return memories

    def delete_memory(self, memory_id: str) -> bool:
        """
        删除记忆

        Args:
            memory_id: 记忆ID

        Returns:
            是否删除成功
        """
        sql = 'DELETE FROM memories WHERE memory_id = ?'
        self.db_manager.execute(sql, (memory_id,))
        self.logger.info(f"记忆删除成功: {memory_id}")
        return True

    def clear_old_memories(self, character_id: str, days: int = 30) -> int:
        """
        清理旧记忆

        Args:
            character_id: 角色ID
            days: 天数

        Returns:
            删除的记忆数量
        """
        cutoff_time = datetime.now() - timedelta(days=days)
        sql = '''
            DELETE FROM memories
            WHERE character_id = ? AND created_at < ?
        '''
        count = self.db_manager.execute(sql, (character_id, cutoff_time.isoformat()))
        self.logger.info(f"清理了 {count} 条旧记忆")
        return count
