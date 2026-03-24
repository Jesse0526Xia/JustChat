"""
虚拟恋人应用主程序
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.managers.config_manager import ConfigManager
from src.managers.database_manager import DatabaseManager
from src.managers.character_manager import CharacterManager
from src.managers.memory_manager import MemoryManager
from src.managers.dialogue_generator import DialogueGenerator
from src.managers.wechat_manager import WeChatManager
from src.utils.logger import LogManager
from src.models.character import CharacterProfile, PersonalityTrait, SpeakingStyle


# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 全局变量
managers = {}


def initialize():
    """初始化应用"""
    logger = LogManager()
    logger.info("应用启动中...")

    # 加载配置
    config_manager = ConfigManager()
    config = config_manager.load_config()

    # 初始化数据库
    db_manager = DatabaseManager(config.database_path)
    db_manager.connect()
    db_manager.initialize_tables()

    # 初始化管理器
    character_manager = CharacterManager(db_manager)
    memory_manager = MemoryManager(db_manager)

    # 初始化对话生成器
    dialogue_generator = DialogueGenerator(
        api_key=config.openai_api_key,
        model=config.dialogue_model,
        character_manager=character_manager,
        memory_manager=memory_manager
    )

    # 初始化微信管理器
    def handle_wechat_message(wechat_msg, character_id):
        """处理微信消息"""
        if not character_id:
            return "请先设置角色"

        try:
            # 生成回复
            response = dialogue_generator.generate_response(
                character_id=character_id,
                user_message=wechat_msg.content
            )

            # 保存对话记忆
            memory_manager.add_dialogue_memory(
                character_id=character_id,
                user_message=wechat_msg.content,
                bot_response=response.content
            )

            return response.content

        except Exception as e:
            logger.error(f"处理微信消息失败: {str(e)}")
            return "抱歉，我现在无法回复。"

    wechat_manager = WeChatManager(
        message_handler=handle_wechat_message,
        config_manager=config_manager,
        max_reconnect_attempts=config.wechat_max_attempts
    )

    # 保存到全局变量
    managers['config'] = config_manager
    managers['database'] = db_manager
    managers['character'] = character_manager
    managers['memory'] = memory_manager
    managers['dialogue'] = dialogue_generator
    managers['wechat'] = wechat_manager
    managers['logger'] = logger

    logger.info("应用初始化完成")


# API路由

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({"status": "ok"})


@app.route('/api/characters', methods=['GET'])
def list_characters():
    """获取角色列表"""
    try:
        characters = managers['character'].list_characters()
        return jsonify({
            "success": True,
            "data": [char.to_dict() for char in characters]
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/characters', methods=['POST'])
def create_character():
    """创建角色"""
    try:
        data = request.json

        # 解析性格特征
        personality_traits = []
        for trait in data.get('personality_traits', []):
            personality_traits.append(PersonalityTrait(trait))

        # 解析说话风格
        speaking_style = SpeakingStyle(data.get('speaking_style', 'casual'))

        # 创建角色档案
        profile = CharacterProfile(
            character_id=data.get('character_id', ''),
            name=data['name'],
            age=data['age'],
            occupation=data.get('occupation', ''),
            background=data.get('background', ''),
            personality_traits=personality_traits,
            avatar_path=data.get('avatar_path'),
            speaking_style=speaking_style
        )

        character_id = managers['character'].create_character(profile)
        return jsonify({
            "success": True,
            "data": {"character_id": character_id}
        })

    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/characters/<character_id>', methods=['GET'])
def get_character(character_id):
    """获取角色详情"""
    try:
        profile = managers['character'].get_character(character_id)
        if not profile:
            return jsonify({"success": False, "message": "角色不存在"}), 404

        return jsonify({
            "success": True,
            "data": profile.to_dict()
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/dialogue', methods=['POST'])
def dialogue():
    """对话接口"""
    try:
        data = request.json

        character_id = data['character_id']
        user_message = data['message']
        dialogue_history = data.get('history', [])

        # 生成回复
        response = managers['dialogue'].generate_response(
            character_id=character_id,
            user_message=user_message,
            dialogue_history=dialogue_history
        )

        # 保存对话记忆
        managers['memory'].add_dialogue_memory(
            character_id=character_id,
            user_message=user_message,
            bot_response=response.content
        )

        return jsonify({
            "success": True,
            "data": response.to_dict()
        })

    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/wechat/login', methods=['POST'])
def wechat_login():
    """微信登录"""
    try:
        enable_qr = request.json.get('enable_qr', False)
        success = managers['wechat'].login(enable_qr=enable_qr)

        return jsonify({
            "success": success,
            "message": "微信登录成功" if success else "微信登录失败"
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/wechat/status', methods=['GET'])
def wechat_status():
    """获取微信状态"""
    return jsonify({
        "success": True,
        "data": {"is_logged_in": managers['wechat'].is_logged_in}
    })


@app.route('/api/wechat/character', methods=['POST'])
def set_wechat_character():
    """设置微信关联角色"""
    try:
        character_id = request.json['character_id']
        managers['wechat'].set_character(character_id)

        return jsonify({
            "success": True,
            "message": "角色设置成功"
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.errorhandler(Exception)
def handle_error(e):
    """全局错误处理"""
    managers['logger'].error(f"Error: {str(e)}")
    return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', port=5000, debug=True)
