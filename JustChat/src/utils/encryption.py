"""
数据加密管理器模块
提供数据加密和解密功能
"""

import base64
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet


class EncryptionManager:
    """数据加密管理器类，提供数据加密和解密功能"""

    def __init__(self, key: Optional[bytes] = None):
        """
        初始化加密管理器

        Args:
            key: 加密密钥，如果未提供则自动生成新密钥
        """
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext: str) -> str:
        """
        加密明文字符串

        Args:
            plaintext: 明文字符串

        Returns:
            Base64编码的密文字符串
        """
        # 将字符串转为bytes
        plaintext_bytes = plaintext.encode('utf-8')
        # 加密
        encrypted_bytes = self.cipher.encrypt(plaintext_bytes)
        # Base64编码转为字符串
        encrypted_str = base64.b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_str

    def decrypt(self, encrypted_str: str) -> str:
        """
        解密密文字符串

        Args:
            encrypted_str: Base64编码的密文字符串

        Returns:
            解密后的明文字符串
        """
        # Base64解码
        encrypted_bytes = base64.b64decode(encrypted_str.encode('utf-8'))
        # 解密
        decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
        # 转为字符串
        decrypted_str = decrypted_bytes.decode('utf-8')
        return decrypted_str

    def save_key(self, key_path: str):
        """
        保存密钥到文件

        Args:
            key_path: 密钥文件路径
        """
        key_file = Path(key_path)
        key_file.parent.mkdir(parents=True, exist_ok=True)
        key_file.write_bytes(self.key)

    @classmethod
    def load_key(cls, key_path: str) -> 'EncryptionManager':
        """
        从文件加载密钥

        Args:
            key_path: 密钥文件路径

        Returns:
            加密管理器实例
        """
        key_file = Path(key_path)
        if not key_file.exists():
            raise FileNotFoundError(f"密钥文件不存在: {key_path}")
        key = key_file.read_bytes()
        return cls(key=key)

    def get_key(self) -> bytes:
        """
        获取当前密钥

        Returns:
            密钥字节
        """
        return self.key
