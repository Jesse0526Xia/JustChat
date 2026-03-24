# 虚拟恋人应用 - 部署文档

## 环境准备

### 系统要求
- Python 3.8 或更高版本
- pip
- Docker (可选)
- OpenAI API Key

### Windows环境
1. 安装Python 3.8+：https://www.python.org/downloads/
2. 安装pip：Python安装包已包含pip
3. 安装Docker Desktop (可选)：https://www.docker.com/products/docker-desktop

## 本地部署

### 1. 克隆代码
```bash
git clone <repository-url>
cd JustChat
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
# 复制环境变量模板
copy config\.env.example config\.env

# 编辑config\.env文件，填入你的OpenAI API Key
OPENAI_API_KEY=your_actual_openai_api_key_here
ENCRYPTION_KEY=your_encryption_key_here
```

### 4. 初始化数据库
启动应用时会自动初始化数据库，无需手动操作。

### 5. 启动应用

#### 仅启动Web服务器
```bash
python main.py --web
```

#### 仅启动微信监听
```bash
python main.py --wechat
```

#### 同时启动Web和微信
```bash
python main.py --all
```

应用启动后：
- Web API地址：http://localhost:5000
- 健康检查：http://localhost:5000/health

## Docker部署

### 1. 构建镜像
```bash
docker-compose build
```

### 2. 配置环境变量
在项目根目录创建`.env`文件：
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
ENCRYPTION_KEY=your_encryption_key_here
```

### 3. 启动服务
```bash
docker-compose up -d
```

### 4. 查看日志
```bash
docker-compose logs -f
```

### 5. 停止服务
```bash
docker-compose down
```

## 云服务器部署

### 使用Supervisor (推荐)

#### 1. 安装Supervisor
```bash
# Ubuntu/Debian
sudo apt-get install supervisor

# CentOS/RHEL
sudo yum install supervisor
```

#### 2. 创建配置文件
创建 `/etc/supervisor/conf.d/virtual_lover.conf`：
```ini
[program:virtual_lover]
command=/usr/bin/python3 /path/to/JustChat/main.py --all
directory=/path/to/JustChat
user=www-data
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/virtual_lover.err.log
stdout_logfile=/var/log/virtual_lover.out.log
environment=OPENAI_API_KEY="your_openai_api_key"
```

#### 3. 启动服务
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start virtual_lover
```

#### 4. 查看状态
```bash
sudo supervisorctl status virtual_lover
```

### 使用Systemd

#### 1. 创建服务文件
创建 `/etc/systemd/system/virtual_lover.service`：
```ini
[Unit]
Description=Virtual Lover Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/JustChat
ExecStart=/usr/bin/python3 /path/to/JustChat/main.py --all
Restart=always
RestartSec=10
Environment="OPENAI_API_KEY=your_openai_api_key"

[Install]
WantedBy=multi-user.target
```

#### 2. 启动服务
```bash
sudo systemctl daemon-reload
sudo systemctl start virtual_lover
sudo systemctl enable virtual_lover
```

#### 3. 查看状态
```bash
sudo systemctl status virtual_lover
```

## Nginx反向代理配置

如果需要通过域名访问，可以配置Nginx反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 数据备份

### 自动备份
系统会自动每天备份数据库到 `backup` 目录。

### 手动备份
```bash
python -c "from src.app import managers; managers['database'].backup()"
```

### 恢复备份
```bash
python -c "from src.app import managers; managers['database'].restore('backup/virtual_lover_20240324_143025.db')"
```

## 常见问题

### 1. 微信登录失败
- 确保网络连接正常
- 尝试使用 `--wechat` 参数单独启动微信
- 检查防火墙设置

### 2. OpenAI API调用失败
- 检查API Key是否正确
- 确认API账户有足够的额度
- 检查网络连接

### 3. 数据库错误
- 检查 `data` 目录是否有写入权限
- 尝试删除数据库文件重新初始化

### 4. Docker容器无法启动
- 检查Docker是否正常运行
- 查看容器日志：`docker-compose logs`
- 确保端口5000未被占用

## 安全建议

1. **保护API Key**：不要将 `.env` 文件提交到版本控制系统
2. **使用HTTPS**：生产环境建议使用SSL证书
3. **限制访问**：使用防火墙限制API访问
4. **定期备份**：定期备份数据库和配置文件
5. **更新依赖**：定期更新Python依赖包

## 性能优化

1. **使用Redis缓存**：对于高并发场景，可以使用Redis替代内存缓存
2. **数据库优化**：为常用查询添加索引
3. **负载均衡**：使用多实例部署和负载均衡
4. **CDN加速**：使用CDN加速静态资源访问

## 监控和日志

### 查看日志
```bash
# 应用日志
tail -f logs/virtual_lover.log

# Supervisor日志
tail -f /var/log/virtual_lover.out.log
```

### 监控指标
- API响应时间
- 对话生成成功率
- 微信连接状态
- 数据库查询性能

## 更新升级

### 更新代码
```bash
git pull
pip install -r requirements.txt
```

### 重启服务
```bash
# Supervisor
sudo supervisorctl restart virtual_lover

# Systemd
sudo systemctl restart virtual_lover

# Docker
docker-compose restart
```
