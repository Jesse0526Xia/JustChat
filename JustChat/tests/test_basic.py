"""
基础功能测试
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.managers.database_manager import DatabaseManager
from src.managers.character_manager import CharacterManager
from src.managers.memory_manager import MemoryManager
from src.models.character import CharacterProfile, PersonalityTrait, SpeakingStyle


def test_database():
    """测试数据库连接"""
    print("测试数据库连接...")
    db = DatabaseManager('data/test.db')
    db.connect()
    db.initialize_tables()
    print("✓ 数据库连接成功")
    db.disconnect()


def test_character_manager():
    """测试角色管理器"""
    print("\n测试角色管理器...")

    db = DatabaseManager('data/test.db')
    db.connect()
    db.initialize_tables()

    character_manager = CharacterManager(db)

    # 创建测试角色
    profile = CharacterProfile(
        character_id='',
        name='测试角色',
        age=22,
        occupation='学生',
        background='这是一个测试角色',
        personality_traits=[PersonalityTrait.GENTLE, PersonalityTrait.ACTIVE],
        speaking_style=SpeakingStyle.CUTE
    )

    character_id = character_manager.create_character(profile)
    print(f"✓ 角色创建成功: {character_id}")

    # 获取角色
    retrieved_profile = character_manager.get_character(character_id)
    assert retrieved_profile is not None
    assert retrieved_profile.name == '测试角色'
    print(f"✓ 角色获取成功: {retrieved_profile.name}")

    # 列出角色
    characters = character_manager.list_characters()
    assert len(characters) > 0
    print(f"✓ 角色列表获取成功: 共{len(characters)}个角色")

    # 删除角色
    character_manager.delete_character(character_id)
    print(f"✓ 角色删除成功")

    db.disconnect()


def test_memory_manager():
    """测试记忆管理器"""
    print("\n测试记忆管理器...")

    db = DatabaseManager('data/test.db')
    db.connect()
    db.initialize_tables()

    memory_manager = MemoryManager(db)

    # 添加测试记忆
    memory_id = memory_manager.add_memory(
        character_id='test_char',
        content='这是一条测试记忆',
        memory_type='custom'
    )
    print(f"✓ 记忆添加成功: {memory_id}")

    # 获取最近记忆
    memories = memory_manager.get_recent_memories('test_char', limit=10)
    print(f"✓ 最近记忆获取成功: 共{len(memories)}条")

    # 搜索记忆
    results = memory_manager.search_memories('test_char', '测试')
    print(f"✓ 记忆搜索成功: 找到{len(results)}条")

    db.disconnect()


def main():
    """运行所有测试"""
    print("=" * 50)
    print("虚拟恋人应用 - 基础功能测试")
    print("=" * 50)

    try:
        test_database()
        test_character_manager()
        test_memory_manager()

        print("\n" + "=" * 50)
        print("✓ 所有测试通过！")
        print("=" * 50)

    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
