# 虚拟恋人应用

一个基于Python的虚拟恋人应用，支持角色定制、记忆管理、故事导入和微信接入等功能。

## 功能特性

- **角色定制**: 可定制角色的身份、性格、经历、人物形象、说话风格等
- **故事导入**: 支持导入TXT、PDF、MD格式的故事文件，作为共同的过去经历
- **记忆管理**: 拥有记忆能力，可以记住对话和经历
- **微信接入**: 可通过微信与虚拟恋人进行对话
- **个性化设置**: 可定制头像、昵称、微信签名等功能
- **持久化运行**: 支持Docker部署，即使关闭电脑，微信仍可正常聊天

## 技术栈

- **后端**: Python 3.8+
- **Web框架**: Flask
- **数据库**: SQLite
- **微信接入**: itchat
- **AI对话**: OpenAI API
- **部署**: Docker + Supervisor

## 快速开始

### 环境准备

- Python 3.8 或更高版本
- pip
- OpenAI API Key

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

```bash
cp config/.env.example config/.env
# 编辑 config/.env，填入你的 OPENAI_API_KEY
```

### 初始化数据库

```bash
python -c "from src.app import initialize; initialize()"
```

### 启动应用

```bash
# 仅启动Web服务器
python main.py --web

# 仅启动微信监听
python main.py --wechat

# 同时启动Web和微信
python main.py --all
```

## Docker部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 项目结构

```
JustChat/
├── src/
│   ├── managers/        # 业务逻辑管理器
│   ├── models/          # 数据模型
│   ├── api/             # REST API端点
│   └── utils/           # 工具类
├── config/              # 配置文件
├── logs/                # 日志文件
├── data/                # 数据文件
├── backup/              # 数据库备份
├── tests/               # 测试用例
├── main.py              # 启动脚本
└── requirements.txt     # 依赖列表
```

## API文档

### 角色管理

- `POST /api/characters` - 创建角色
- `GET /api/characters` - 获取角色列表
- `GET /api/characters/{id}` - 获取角色详情
- `PUT /api/characters/{id}` - 更新角色
- `DELETE /api/characters/{id}` - 删除角色

### 故事管理

- `POST /api/characters/{id}/stories/import` - 导入故事
- `GET /api/characters/{id}/stories` - 获取故事列表
- `GET /api/characters/{id}/stories/search` - 搜索故事

### 记忆管理

- `GET /api/characters/{id}/memories` - 获取记忆列表
- `GET /api/characters/{id}/memories/search` - 搜索记忆
- `DELETE /api/memories/{id}` - 删除记忆

### 微信管理

- `POST /api/wechat/login` - 登录微信
- `GET /api/wechat/status` - 获取登录状态
- `POST /api/wechat/avatar` - 设置头像
- `POST /api/wechat/nickname` - 设置昵称
- `POST /api/wechat/signature` - 设置签名

## 注意事项

### OpenAI API Key
- 需要申请OpenAI API Key才能使用对话功能
- 注意API调用会产生费用，建议设置使用限制
- 妥善保管API Key，不要泄露给他人
- 定期检查API使用量和费用

### 微信接入
- itchat库可能不稳定，建议使用小号测试
- 注意微信风控，避免频繁操作
- 微信可能会限制账号功能，请合理使用
- 建议不要在主微信号上使用

### 数据安全
- 定期备份数据库和配置文件
- 敏感信息已加密存储，但仍需注意安全
- 不要将 `.env` 文件提交到版本控制系统
- 生产环境建议使用HTTPS

### 性能监控
- 监控API响应时间，及时优化
- 监控数据库性能，必要时添加索引
- 监控内存使用情况，避免内存泄漏
- 定期清理旧记忆和日志文件

### 系统要求
- Python 3.8 或更高版本
- 建议使用Linux服务器进行部署
- Windows环境也可以运行，但建议使用WSL
- 确保网络连接稳定

### 常见问题
- 如果微信登录失败，尝试重新扫码
- 如果对话生成失败，检查API Key是否正确
- 如果数据库错误，检查文件权限
- 如果Docker无法启动，检查端口占用

## 许可证

MIT License
