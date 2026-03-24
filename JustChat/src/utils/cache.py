"""
缓存管理器模块
提供内存缓存功能
"""

import time
from typing import Any, Optional, Dict, Tuple


class CacheManager:
    """缓存管理器类，提供内存缓存功能"""

    def __init__(self, ttl: int = 3600):
        """
        初始化缓存管理器

        Args:
            ttl: 缓存生存时间（秒），默认3600秒（1小时）
        """
        self.ttl = ttl
        self.cache: Dict[str, Tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值

        Args:
            key: 缓存键

        Returns:
            缓存值，如果不存在或已过期则返回None
        """
        if key in self.cache:
            value, timestamp = self.cache[key]
            # 检查是否过期
            if time.time() - timestamp < self.ttl:
                return value
            else:
                # 已过期，删除
                del self.cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        设置缓存值

        Args:
            key: 缓存键
            value: 缓存值
            ttl: 自定义生存时间（秒），如果为None则使用类默认值
        """
        timestamp = time.time()
        self.cache[key] = (value, timestamp)

    def delete(self, key: str) -> bool:
        """
        删除缓存值

        Args:
            key: 缓存键

        Returns:
            是否成功删除
        """
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def clear(self):
        """清空所有缓存"""
        self.cache.clear()

    def exists(self, key: str) -> bool:
        """
        检查缓存键是否存在且未过期

        Args:
            key: 缓存键

        Returns:
            是否存在且未过期
        """
        return self.get(key) is not None

    def cleanup_expired(self) -> int:
        """
        清理所有过期的缓存

        Returns:
            清理的缓存项数量
        """
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp >= self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
        return len(expired_keys)

    def size(self) -> int:
        """
        获取缓存项数量

        Returns:
            缓存项数量
        """
        return len(self.cache)

    def get_all(self) -> Dict[str, Any]:
        """
        获取所有未过期的缓存项

        Returns:
            缓存项字典
        """
        result = {}
        current_time = time.time()
        for key, (value, timestamp) in self.cache.items():
            if current_time - timestamp < self.ttl:
                result[key] = value
        return result
