"""
对话生成器模块
"""

import time
from datetime import datetime
from typing import List, Dict, Optional, Any

import openai

from src.managers.character_manager import CharacterManager
from src.managers.memory_manager import MemoryManager
from src.models.character import CharacterProfile
from src.models.memory import Memory
from src.utils.logger import LogManager


class DialogueResponse:
    """对话响应数据类"""

    def __init__(self, content: str, generation_time: float, tokens_used: int, model: str):
        self.content = content
        self.generation_time = generation_time
        self.tokens_used = tokens_used
        self.model = model
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'content': self.content,
            'generation_time': self.generation_time,
            'tokens_used': self.tokens_used,
            'model': self.model,
            'timestamp': self.timestamp.isoformat()
        }


class DialogueGenerator:
    """对话生成器类"""

    def __init__(self, api_key: str, model: str = 'gpt-3.5-turbo',
                 character_manager: Optional[CharacterManager] = None,
                 memory_manager: Optional[MemoryManager] = None):
        """
        初始化对话生成器

        Args:
            api_key: OpenAI API密钥
            model: 使用的模型
            character_manager: 角色管理器
            memory_manager: 记忆管理器
        """
        openai.api_key = api_key
        self.model = model
        self.character_manager = character_manager
        self.memory_manager = memory_manager
        self.logger = LogManager()

    def build_system_prompt(self, profile: CharacterProfile) -> str:
        """
        构建系统提示词

        Args:
            profile: 角色档案

        Returns:
            系统提示词
        """
        traits_str = ", ".join([trait.value for trait in profile.personality_traits])

        prompt = f"""你叫{profile.name}，今年{profile.age}岁，职业是{profile.occupation}。

性格特征：{traits_str}

背景故事：{profile.background}

说话风格：使用{profile.speaking_style.value}的说话风格。

请保持角色设定，根据用户输入和记忆生成回复。"""
        return prompt

    def incorporate_memories(self, recent_memories: List[Memory],
                            dialogue_history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        整合记忆到对话上下文

        Args:
            recent_memories: 最近的记忆列表
            dialogue_history: 对话历史

        Returns:
            完整的对话消息列表
        """
        messages = []

        # 将记忆转换为消息格式
        for memory in recent_memories[:5]:  # 最多取5条记忆
            messages.append({
                "role": "assistant",
                "content": f"[记忆] {memory.content}"
            })

        # 添加对话历史
        messages.extend(dialogue_history)

        return messages

    def apply_speaking_style(self, content: str, style: str) -> str:
        """
        应用说话风格

        Args:
            content: 原始内容
            style: 说话风格

        Returns:
            调整后的内容
        """
        if style == "cute":
            # 可爱风格：添加表情符号
            emojis = ["😊", "✨", "💕", "🥰", "😄"]
            import random
            content = content.rstrip("。！？")
            content += random.choice(emojis)
        elif style == "formal":
            # 正式风格：使用礼貌用语
            content = content.replace("你", "您")
        elif style == "romantic":
            # 浪漫风格：添加甜蜜词汇
            terms = ["亲爱的", "宝贝"]
            import random
            if random.random() > 0.5:
                content = terms[0] + "，" + content

        return content

    def generate_response(self, character_id: str, user_message: str,
                         dialogue_history: Optional[List[Dict[str, str]]] = None) -> DialogueResponse:
        """
        生成对话回复

        Args:
            character_id: 角色ID
            user_message: 用户消息
            dialogue_history: 对话历史

        Returns:
            对话响应

        Raises:
            ValueError: 角色不存在时抛出异常
            RuntimeError: API调用失败时抛出异常
        """
        # 获取角色信息
        if not self.character_manager:
            raise RuntimeError("角色管理器未初始化")

        profile = self.character_manager.get_character(character_id)
        if not profile:
            raise ValueError(f"角色不存在: {character_id}")

        # 检索相关记忆
        recent_memories = []
        if self.memory_manager:
            recent_memories = self.memory_manager.retrieve_relevant_memories(
                character_id, user_message, top_k=5
            )

        # 构建系统提示词
        system_prompt = self.build_system_prompt(profile)

        # 构建对话上下文
        messages = [{"role": "system", "content": system_prompt}]

        # 整合记忆
        if recent_memories:
            messages.extend(self.incorporate_memories(recent_memories, dialogue_history or []))
        elif dialogue_history:
            messages.extend(dialogue_history)

        # 添加用户消息
        messages.append({"role": "user", "content": user_message})

        try:
            # 调用OpenAI API
            start_time = time.time()
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            generation_time = time.time() - start_time

            # 提取回复内容
            content = response.choices[0].message.content

            # 应用说话风格
            content = self.apply_speaking_style(content, profile.speaking_style.value)

            # 计算token使用量
            tokens_used = response.usage.total_tokens

            # 创建响应对象
            dialogue_response = DialogueResponse(
                content=content,
                generation_time=generation_time,
                tokens_used=tokens_used,
                model=self.model
            )

            self.logger.info(f"对话生成成功: {character_id}, 耗时: {generation_time:.2f}s")
            return dialogue_response

        except Exception as e:
            self.logger.error(f"对话生成失败: {str(e)}")
            raise RuntimeError(f"对话生成失败: {str(e)}")
