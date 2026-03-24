# 虚拟恋人应用 - 使用文档

## 简介

虚拟恋人应用是一个基于AI的对话系统，支持角色定制、记忆管理、故事导入和微信接入等功能。你可以创建一个独一无二的虚拟恋人，通过微信与他/她进行对话。

## 快速开始

### 1. 创建角色

使用API创建你的第一个虚拟恋人：

```bash
curl -X POST http://localhost:5000/api/characters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "小雅",
    "age": 22,
    "occupation": "大学生",
    "background": "来自南方的小镇，性格温柔善良，喜欢读书和旅行。",
    "personality_traits": ["gentle", "active"],
    "speaking_style": "cute"
  }'
```

响应示例：
```json
{
  "success": true,
  "data": {
    "character_id": "a1b2c3d4e5f6g7h8"
  }
}
```

### 2. 通过微信对话

1. 启动微信监听：
```bash
python main.py --wechat
```

2. 扫描二维码登录微信

3. 设置关联角色：
```bash
curl -X POST http://localhost:5000/api/wechat/character \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": "a1b2c3d4e5f6g7h8"
  }'
```

4. 现在你可以通过微信与虚拟恋人对话了！

## API文档

### 角色管理

#### 创建角色
```
POST /api/characters
```

请求体：
```json
{
  "name": "角色名称",
  "age": 22,
  "occupation": "职业",
  "background": "背景故事",
  "personality_traits": ["gentle", "active"],
  "speaking_style": "cute"
}
```

性格特征选项：
- `gentle` - 温柔
- `active` - 活泼
- `introverted` - 内向
- `humorous` - 幽默
- `serious` - 严肃

说话风格选项：
- `formal` - 正式
- `cute` - 可爱
- `casual` - 随意
- `romantic` - 浪漫

#### 获取角色列表
```
GET /api/characters
```

#### 获取角色详情
```
GET /api/characters/{character_id}
```

### 对话接口

#### 发送消息
```
POST /api/dialogue
```

请求体：
```json
{
  "character_id": "a1b2c3d4e5f6g7h8",
  "message": "你好，今天天气怎么样？",
  "history": []
}
```

响应示例：
```json
{
  "success": true,
  "data": {
    "content": "今天是晴天呢，很适合出去走走哦~ 😊",
    "generation_time": 1.23,
    "tokens_used": 45,
    "model": "gpt-3.5-turbo",
    "timestamp": "2024-03-24T14:30:25"
  }
}
```

### 微信管理

#### 登录微信
```
POST /api/wechat/login
```

请求体：
```json
{
  "enable_qr": true
}
```

#### 获取登录状态
```
GET /api/wechat/status
```

#### 设置关联角色
```
POST /api/wechat/character
```

请求体：
```json
{
  "character_id": "a1b2c3d4e5f6g7h8"
}
```

## 使用示例

### Python示例

```python
import requests

API_BASE = "http://localhost:5000"

# 1. 创建角色
response = requests.post(f"{API_BASE}/api/characters", json={
    "name": "小明",
    "age": 25,
    "occupation": "程序员",
    "background": "热爱编程，喜欢探索新技术。",
    "personality_traits": ["humorous", "active"],
    "speaking_style": "casual"
})
character_id = response.json()["data"]["character_id"]

# 2. 发送消息
response = requests.post(f"{API_BASE}/api/dialogue", json={
    "character_id": character_id,
    "message": "你好，介绍一下你自己吧！"
})
print(response.json()["data"]["content"])
```

### JavaScript示例

```javascript
const API_BASE = "http://localhost:5000";

// 创建角色
async function createCharacter() {
  const response = await fetch(`${API_BASE}/api/characters`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: "小红",
      age: 23,
      occupation: "设计师",
      background: "热爱艺术，喜欢创作。",
      personality_traits: ["gentle", "introverted"],
      speaking_style: "cute"
    })
  });
  const data = await response.json();
  return data.data.character_id;
}

// 发送消息
async function sendMessage(characterId, message) {
  const response = await fetch(`${API_BASE}/api/dialogue`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      character_id: characterId,
      message: message
    })
  });
  const data = await response.json();
  return data.data.content;
}

// 使用示例
(async () => {
  const characterId = await createCharacter();
  const reply = await sendMessage(characterId, "你好！");
  console.log(reply);
})();
```

## 功能特性

### 1. 角色定制
- 自定义姓名、年龄、职业
- 设置背景故事
- 选择性格特征
- 配置说话风格

### 2. 记忆系统
- 自动保存对话历史
- 智能检索相关记忆
- 影响对话生成

### 3. 说话风格
不同的说话风格会产生不同的回复效果：
- **可爱风格**：使用表情符号和叠词
- **正式风格**：使用礼貌用语
- **随意风格**：口语化表达
- **浪漫风格**：添加甜蜜词汇

### 4. 微信接入
- 通过微信与虚拟恋人对话
- 自动回复消息
- 保存对话记忆

## 最佳实践

### 1. 设计角色档案
- 提供详细的背景故事
- 选择合适的性格特征
- 根据角色特点选择说话风格

### 2. 对话技巧
- 保持对话的自然流畅
- 适当引导话题
- 尊重角色设定

### 3. 记忆管理
- 系统会自动保存重要对话
- 可以通过API查看和管理记忆
- 定期清理旧记忆以保持性能

## 常见问题

### Q: 如何修改角色信息？
A: 目前需要删除后重新创建角色。未来版本将支持在线编辑。

### Q: 对话回复慢怎么办？
A: 检查网络连接和OpenAI API响应时间。可以考虑升级到更快的模型。

### Q: 微信无法登录怎么办？
A: 确保网络连接正常，尝试重新扫码登录。

### Q: 如何导出对话记录？
A: 对话记录保存在数据库中，可以通过API查询记忆数据。

### Q: 支持多用户吗？
A: 每个微信账号可以关联一个角色。多用户需要部署多个实例。

## 技术支持

如有问题，请查看：
- 部署文档：`docs/DEPLOYMENT.md`
- 项目README：`README.md`
- 提交Issue：GitHub Issues

## 更新日志

### v1.0.0 (2024-03-24)
- 初始版本发布
- 支持角色创建和管理
- 支持对话生成
- 支持微信接入
- 支持记忆管理

## 许可证

MIT License
