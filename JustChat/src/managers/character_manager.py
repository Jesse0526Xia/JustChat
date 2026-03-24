"""
角色管理器模块
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from src.managers.database_manager import DatabaseManager
from src.models.character import CharacterProfile, PersonalityTrait, SpeakingStyle
from src.models.role import RoleModel
from src.utils.logger import LogManager


class CharacterManager:
    """角色管理器类"""

    def __init__(self, db_manager: DatabaseManager):
        """
        初始化角色管理器

        Args:
            db_manager: 数据库管理器
        """
        self.db_manager = db_manager
        self.logger = LogManager()

    def validate_profile(self, profile: CharacterProfile) -> bool:
        """
        验证角色档案

        Args:
            profile: 角色档案

        Returns:
            是否验证通过

        Raises:
            ValueError: 验证失败时抛出异常
        """
        # 验证姓名
        if not (1 <= len(profile.name) <= 50):
            raise ValueError("姓名长度必须在1-50字符之间")

        # 验证年龄
        if not (18 <= profile.age <= 100):
            raise ValueError("年龄必须在18-100之间")

        # 验证性格特征
        if not profile.personality_traits:
            raise ValueError("性格特征不能为空")

        for trait in profile.personality_traits:
            if not isinstance(trait, PersonalityTrait):
                raise ValueError(f"无效的性格特征: {trait}")

        # 验证头像
        if profile.avatar_path:
            avatar_path = Path(profile.avatar_path)
            if not avatar_path.exists():
                raise ValueError(f"头像文件不存在: {profile.avatar_path}")

            file_size = avatar_path.stat().st_size
            if file_size > 5 * 1024 * 1024:  # 5MB
                raise ValueError("头像文件大小不能超过5MB")

        # 验证说话风格
        if not isinstance(profile.speaking_style, SpeakingStyle):
            raise ValueError(f"无效的说话风格: {profile.speaking_style}")

        return True

    def create_character(self, profile: CharacterProfile) -> str:
        """
        创建新角色

        Args:
            profile: 角色档案

        Returns:
            角色ID

        Raises:
            ValueError: 验证失败时抛出异常
        """
        # 验证档案
        self.validate_profile(profile)

        # 生成角色ID
        if not profile.character_id:
            profile.character_id = uuid.uuid4().hex

        # 设置时间戳
        now = datetime.now()
        profile.created_at = now
        profile.updated_at = now

        # 创建角色模型
        role_model = RoleModel(
            character_id=profile.character_id,
            name=profile.name,
            age=profile.age,
            occupation=profile.occupation,
            background=profile.background,
            personality_traits=[trait.value for trait in profile.personality_traits],
            avatar_path=profile.avatar_path,
            speaking_style=profile.speaking_style.value,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

        # 插入数据库
        sql = '''
            INSERT INTO roles (
                character_id, name, age, occupation, background,
                personality_traits, avatar_path, speaking_style,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.db_manager.execute(sql, role_model.to_db_tuple())

        self.logger.info(f"角色创建成功: {profile.name} ({profile.character_id})")
        return profile.character_id

    def get_character(self, character_id: str) -> Optional[CharacterProfile]:
        """
        获取角色信息

        Args:
            character_id: 角色ID

        Returns:
            角色档案，如果不存在则返回None
        """
        sql = 'SELECT * FROM roles WHERE character_id = ?'
        row = self.db_manager.fetch_one(sql, (character_id,))

        if not row:
            return None

        role_model = RoleModel.from_db_row(row)

        # 转换为CharacterProfile
        profile = CharacterProfile(
            character_id=role_model.character_id,
            name=role_model.name,
            age=role_model.age,
            occupation=role_model.occupation,
            background=role_model.background,
            personality_traits=[
                PersonalityTrait(trait) for trait in role_model.personality_traits
            ],
            avatar_path=role_model.avatar_path,
            speaking_style=SpeakingStyle(role_model.speaking_style),
            created_at=role_model.created_at,
            updated_at=role_model.updated_at
        )

        return profile

    def update_character(self, character_id: str, profile: CharacterProfile) -> bool:
        """
        更新角色信息

        Args:
            character_id: 角色ID
            profile: 新的角色档案

        Returns:
            是否更新成功

        Raises:
            ValueError: 角色不存在或验证失败时抛出异常
        """
        # 验证角色存在
        if not self.get_character(character_id):
            raise ValueError(f"角色不存在: {character_id}")

        # 验证档案
        self.validate_profile(profile)

        # 更新时间戳
        profile.updated_at = datetime.now()

        # 更新数据库
        role_model = RoleModel(
            character_id=character_id,
            name=profile.name,
            age=profile.age,
            occupation=profile.occupation,
            background=profile.background,
            personality_traits=[trait.value for trait in profile.personality_traits],
            avatar_path=profile.avatar_path,
            speaking_style=profile.speaking_style.value,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

        sql = '''
            UPDATE roles SET
                name = ?, age = ?, occupation = ?, background = ?,
                personality_traits = ?, avatar_path = ?, speaking_style = ?,
                updated_at = ?
            WHERE character_id = ?
        '''
        self.db_manager.execute(sql, (
            role_model.name,
            role_model.age,
            role_model.occupation,
            role_model.background,
            role_model.personality_traits_json,
            role_model.avatar_path,
            role_model.speaking_style,
            role_model.updated_at.isoformat(),
            character_id
        ))

        self.logger.info(f"角色更新成功: {profile.name} ({character_id})")
        return True

    def delete_character(self, character_id: str) -> bool:
        """
        删除角色

        Args:
            character_id: 角色ID

        Returns:
            是否删除成功

        Raises:
            ValueError: 角色不存在时抛出异常
        """
        # 验证角色存在
        if not self.get_character(character_id):
            raise ValueError(f"角色不存在: {character_id}")

        # 删除数据库记录（级联删除相关记忆和故事）
        sql = 'DELETE FROM roles WHERE character_id = ?'
        self.db_manager.execute(sql, (character_id,))

        self.logger.info(f"角色删除成功: {character_id}")
        return True

    def list_characters(self) -> List[CharacterProfile]:
        """
        列出所有角色

        Returns:
            角色档案列表
        """
        sql = 'SELECT * FROM roles ORDER BY created_at DESC'
        rows = self.db_manager.fetch_all(sql)

        profiles = []
        for row in rows:
            role_model = RoleModel.from_db_row(row)
            profile = CharacterProfile(
                character_id=role_model.character_id,
                name=role_model.name,
                age=role_model.age,
                occupation=role_model.occupation,
                background=role_model.background,
                personality_traits=[
                    PersonalityTrait(trait) for trait in role_model.personality_traits
                ],
                avatar_path=role_model.avatar_path,
                speaking_style=SpeakingStyle(role_model.speaking_style),
                created_at=role_model.created_at,
                updated_at=role_model.updated_at
            )
            profiles.append(profile)

        return profiles
