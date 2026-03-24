# 虚拟恋人应用 - 快速启动指南

## 5分钟快速开始

### 第一步：安装依赖

```bash
pip install -r requirements.txt
```

### 第二步：配置API Key

1. 复制环境变量模板：
```bash
copy config\.env.example config\.env
```

2. 编辑 `config\.env` 文件，填入你的OpenAI API Key：
```
OPENAI_API_KEY=sk-your-actual-api-key-here
ENCRYPTION_KEY=your-encryption-key
```

### 第三步：启动应用

```bash
python main.py --all
```

### 第四步：使用API

创建你的第一个虚拟恋人：

```bash
curl -X POST http://localhost:5000/api/characters ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"小雅\",\"age\":22,\"occupation\":\"大学生\",\"background\":\"来自南方的小镇，性格温柔善良。\",\"personality_traits\":[\"gentle\",\"active\"],\"speaking_style\":\"cute\"}"
```

发送消息：

```bash
curl -X POST http://localhost:5000/api/dialogue ^
  -H "Content-Type: application/json" ^
  -d "{\"character_id\":\"你的角色ID\",\"message\":\"你好，介绍一下你自己吧！\"}"
```

### 第五步：微信接入

1. 等待微信登录二维码出现
2. 使用微信扫描二维码登录
3. 设置关联角色：
```bash
curl -X POST http://localhost:5000/api/wechat/character ^
  -H "Content-Type: application/json" ^
  -d "{\"character_id\":\"你的角色ID\"}"
```
4. 现在可以通过微信与虚拟恋人对话了！

## 常用命令

```bash
# 仅启动Web服务
python main.py --web

# 仅启动微信监听
python main.py --wechat

# 同时启动Web和微信
python main.py --all

# 运行测试
python tests/test_basic.py

# Docker部署
docker-compose up -d
```

## 项目结构

```
JustChat/
├── src/                    # 源代码
│   ├── managers/          # 业务逻辑管理器
│   ├── models/            # 数据模型
│   ├── utils/             # 工具类
│   └── app.py             # 主应用
├── config/                # 配置文件
├── docs/                  # 文档
├── tests/                 # 测试
├── main.py               # 启动脚本
└── requirements.txt      # 依赖列表
```

## 下一步

- 查看 [使用文档](docs/USAGE.md) 了解更多API使用方法
- 查看 [部署文档](docs/DEPLOYMENT.md) 了解部署方案
- 查看 [README.md](README.md) 了解项目详情

## 获取帮助

如有问题，请查看：
- 常见问题：docs/USAGE.md
- 部署指南：docs/DEPLOYMENT.md
- 项目主页：README.md
