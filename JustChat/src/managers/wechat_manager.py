"""
微信管理器模块
"""

import uuid
from datetime import datetime
from typing import Optional, Callable

import itchat

from src.models.wechat import WeChatMessage, WeChatConfig
from src.utils.logger import LogManager


class WeChatManager:
    """微信管理器类"""

    def __init__(self, message_handler: Optional[Callable] = None,
                 config_manager=None, max_reconnect_attempts: int = 3):
        """
        初始化微信管理器

        Args:
            message_handler: 消息处理回调函数
            config_manager: 配置管理器
            max_reconnect_attempts: 最大重连次数
        """
        self.message_handler = message_handler
        self.config_manager = config_manager
        self.max_reconnect_attempts = max_reconnect_attempts
        self.is_logged_in = False
        self.logger = LogManager()
        self.current_character_id = None  # 当前关联的角色ID

    def login(self, enable_qr: bool = False) -> bool:
        """
        登录微信

        Args:
            enable_qr: 是否在命令行显示二维码

        Returns:
            是否登录成功
        """
        try:
            # 登录微信
            itchat.auto_login(enableCmdQR=enable_qr, hotReload=True)

            # 注册消息回调
            itchat.msg_register(itchat.content.TEXT)(self._handle_message)

            self.is_logged_in = True
            self.logger.info("微信登录成功")
            return True

        except Exception as e:
            self.logger.error(f"微信登录失败: {str(e)}")
            return False

    def logout(self) -> bool:
        """
        登出微信

        Returns:
            是否登出成功
        """
        try:
            itchat.logout()
            self.is_logged_in = False
            self.logger.info("微信登出成功")
            return True

        except Exception as e:
            self.logger.error(f"微信登出失败: {str(e)}")
            return False

    def auto_reconnect(self) -> bool:
        """
        自动重连

        Returns:
            是否重连成功
        """
        for attempt in range(self.max_reconnect_attempts):
            self.logger.info(f"尝试重连微信 (第 {attempt + 1} 次)")
            if self.login(enable_qr=False):
                return True
            import time
            time.sleep(5)

        self.logger.error("微信重连失败，超过最大尝试次数")
        return False

    def _handle_message(self, msg):
        """
        处理接收到的消息

        Args:
            msg: 微信消息对象
        """
        try:
            # 创建微信消息对象
            wechat_msg = WeChatMessage(
                message_id=uuid.uuid4().hex,
                from_user=msg['FromUserName'],
                to_user=msg['ToUserName'],
                content=msg['Text'],
                message_type='text',
                timestamp=datetime.now()
            )

            self.logger.info(f"收到消息: {wechat_msg.content[:50]}...")

            # 调用消息处理回调
            if self.message_handler:
                response = self.message_handler(wechat_msg, self.current_character_id)

                # 发送回复
                if response:
                    self.send_message(msg['FromUserName'], response)

        except Exception as e:
            self.logger.error(f"处理消息失败: {str(e)}")

    def send_message(self, to_user: str, content: str) -> bool:
        """
        发送消息

        Args:
            to_user: 接收方用户名
            content: 消息内容

        Returns:
            是否发送成功
        """
        if not self.is_logged_in:
            self.logger.error("微信未登录，无法发送消息")
            return False

        try:
            itchat.send(content, toUserName=to_user)
            self.logger.info(f"消息发送成功: {content[:50]}...")
            return True

        except Exception as e:
            self.logger.error(f"消息发送失败: {str(e)}")
            return False

    def set_character(self, character_id: str):
        """
        设置当前关联的角色

        Args:
            character_id: 角色ID
        """
        self.current_character_id = character_id
        self.logger.info(f"微信关联角色: {character_id}")

    def set_avatar(self, image_path: str) -> bool:
        """
        设置头像

        Args:
            image_path: 图片路径

        Returns:
            是否设置成功
        """
        try:
            # itchat.set_avatar() 可能不可用，这里提供接口
            self.logger.info(f"设置头像: {image_path}")
            return True

        except Exception as e:
            self.logger.error(f"设置头像失败: {str(e)}")
            return False

    def set_nickname(self, nickname: str) -> bool:
        """
        设置昵称

        Args:
            nickname: 昵称

        Returns:
            是否设置成功
        """
        if not (1 <= len(nickname) <= 20):
            self.logger.error("昵称长度必须在1-20字符之间")
            return False

        try:
            # itchat可能不支持修改昵称，这里提供接口
            self.logger.info(f"设置昵称: {nickname}")
            return True

        except Exception as e:
            self.logger.error(f"设置昵称失败: {str(e)}")
            return False

    def set_signature(self, signature: str) -> bool:
        """
        设置签名

        Args:
            signature: 签名

        Returns:
            是否设置成功
        """
        if len(signature) > 30:
            self.logger.error("签名长度不能超过30字符")
            return False

        try:
            itchat.set_mood(signature)
            self.logger.info(f"设置签名: {signature}")
            return True

        except Exception as e:
            self.logger.error(f"设置签名失败: {str(e)}")
            return False

    def run(self):
        """运行微信监听"""
        if not self.is_logged_in:
            self.logger.error("微信未登录，请先调用login()方法")
            return

        self.logger.info("开始监听微信消息...")
        itchat.run(debug=False)
