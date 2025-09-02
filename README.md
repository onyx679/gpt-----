# GPT充值系统 (Python版本)

## 🌟 项目简介

这是一个专业的ChatGPT Plus充值系统，已从PHP版本转换为Python Flask框架，具备相同的功能和界面体验。

### ✨ 主要特性

- 🛡️ **安全可靠**: 完整的错误处理和用户友好的提示信息
- 🚀 **高性能**: 基于Flask框架，轻量级高效
- 📱 **响应式设计**: 支持PC、平板、手机等各种设备
- 🔄 **智能检测**: 自动识别卡密激活状态
- 📊 **日志记录**: 完整的操作日志和错误追踪
- 🎯 **易于部署**: 一键启动脚本，零配置运行

### 🆕 Python版本优势

- ✅ **无需PHP环境**: 只需Python即可运行
- ✅ **跨平台兼容**: Windows、macOS、Linux通用
- ✅ **依赖管理**: 使用pip自动管理依赖包
- ✅ **开发友好**: 热重载，开发调试更便捷

## 🚀 快速开始

### 前置要求

- Python 3.8+ 
- pip (Python包管理器)

### 一键启动

1. **下载并进入项目目录**
   ```bash
   cd gpt充值简易版
   ```

2. **安装依赖并启动**
   ```bash
   # 安装依赖
   python start.py --install
   
   # 启动开发服务器
   python start.py --mode dev
   ```

3. **访问应用**
   打开浏览器访问: http://localhost:5000

### 详细安装步骤

如果一键启动遇到问题，可以按照以下步骤手动安装：

1. **检查环境**
   ```bash
   python start.py --check
   ```

2. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动应用**
   ```bash
   # 开发模式（推荐）
   python start.py --mode dev
   
   # 生产模式
   python start.py --mode prod
   ```

## 📖 使用说明

### 功能流程

1. **验证激活码**: 输入格式为 `CARD-XXXX-XXXX-XXXX` 的激活码
2. **用户信息**: 系统显示激活码状态和绑定邮箱
3. **操作选择**:
   - **新用户**: 粘贴ChatGPT的JSON Token进行首次充值
   - **老用户**: 复用之前的充值记录或更新Token
4. **完成**: 显示操作结果和详细信息

### 界面说明

- 🔵 **步骤指示器**: 清晰显示当前进度
- 📝 **智能表单**: 自动验证输入格式
- 💡 **友好提示**: 用户友好的错误信息
- 🎨 **现代界面**: 使用Tailwind CSS美化界面

## 🔧 高级配置

### 环境变量

创建 `.env` 文件来自定义配置：

```bash
# Flask配置
SECRET_KEY=your-secret-key-here
DEBUG=False
FLASK_ENV=production

# API配置
CHONGZHI_BASE_URL=https://chongzhi.pro
REQUEST_TIMEOUT=30

# 安全配置
SESSION_TIMEOUT=1800
```

### 日志配置

应用会自动创建日志文件：
- `gpt_recharge.log`: 应用日志
- `logs/access.log`: 访问日志（生产模式）
- `logs/error.log`: 错误日志（生产模式）

## 🛠️ 开发指南

### 项目结构

```
gpt充值简易版/
├── app.py                 # Flask主应用
├── api_client.py          # API客户端类
├── error_mappings.py      # 错误信息映射
├── start.py               # 启动脚本
├── requirements.txt       # Python依赖
├── README.md              # 项目文档
├── templates/             # HTML模板
│   ├── index.html         # 主页面
│   └── error.html         # 错误页面
├── static/                # 静态文件
├── logs/                  # 日志目录
└── gpt_recharge.log       # 应用日志
```

### API接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/verify-code` | POST | 验证激活码 |
| `/api/submit-json` | POST | 提交JSON Token |
| `/api/reuse-record` | POST | 复用充值记录 |
| `/api/update-token` | POST | 更新Token |
| `/api/health` | GET | 健康检查 |

### 开发调试

```bash
# 检查系统状态
python start.py --status

# 开发模式（支持热重载）
python start.py --mode dev

# 查看日志
tail -f gpt_recharge.log
```

## 🔒 安全特性

- ✅ **输入验证**: 严格验证激活码格式
- ✅ **错误处理**: 友好的错误信息，不暴露技术细节
- ✅ **会话管理**: 安全的Flask Session
- ✅ **日志记录**: 完整的操作审计日志
- ✅ **HTTPS支持**: 生产环境支持SSL/TLS

## 🚀 生产部署

### 使用Gunicorn部署

```bash
# 启动生产服务器
python start.py --mode prod

# 或直接使用gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🐛 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   netstat -tulpn | grep :5000
   
   # 修改端口（在app.py中）
   app.run(port=8000)
   ```

2. **依赖安装失败**
   ```bash
   # 使用国内镜像源
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. **Python版本问题**
   ```bash
   # 检查Python版本
   python --version
   
   # 如果版本过低，请升级到Python 3.8+
   ```

4. **权限问题**
   ```bash
   # Windows用户可能需要以管理员身份运行
   # Linux/macOS用户可能需要使用sudo
   ```

### 日志查看

```bash
# 查看应用日志
cat gpt_recharge.log

# 实时监控日志
tail -f gpt_recharge.log

# 查看错误日志
grep "ERROR" gpt_recharge.log
```

## 📞 支持与反馈

如果遇到问题或有改进建议，请：

1. 查看项目日志文件
2. 检查是否按照文档正确配置
3. 确认Python环境和依赖包版本

## 🔄 版本对比

| 特性 | PHP版本 | Python版本 |
|------|---------|------------|
| 运行环境 | 需要PHP+Web服务器 | 只需Python |
| 依赖管理 | 手动管理 | pip自动管理 |
| 跨平台 | 需配置Web服务器 | 原生跨平台 |
| 开发调试 | 需配置开发环境 | 一键启动 |
| 日志系统 | 基础日志 | 完整日志系统 |

## ⚠️ 免责声明

本系统仅供学习和研究使用，请遵守相关法律法规。使用本系统产生的任何问题，开发者不承担责任。

---

**✨ 享受Python版本带来的便捷体验！**