# 🚀 GPT充值系统

一个基于Flask的ChatGPT Plus充值系统，支持一键部署到Vercel。

## ✨ 特性

- 🛡️ 安全的激活码验证
- 🔄 智能充值记录管理  
- 📱 响应式现代界面
- ⚡ Serverless架构，零运维

## 🌐 在线演示

部署后访问你的Vercel域名即可使用

## 🚀 一键部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/gpt-recharge)

## 📋 部署步骤

1. **Fork此仓库**
2. **在Vercel中导入项目**
3. **设置环境变量**：
   - `SECRET_KEY`: 设置一个安全的密钥
   - `SESSION_TIMEOUT`: `1800` (可选)
4. **部署完成**

## 🔧 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `SECRET_KEY` | Flask应用密钥 | ✅ |
| `SESSION_TIMEOUT` | 会话超时时间(秒) | ❌ |

## 📁 项目结构

```
├── api/
│   └── index.py          # Vercel入口文件
├── templates/            # HTML模板
├── static/              # 静态文件
├── api_client.py        # API客户端
├── error_mappings.py    # 错误处理
├── requirements.txt     # Python依赖
└── vercel.json         # Vercel配置
```

## 🛠️ 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
cd api && python index.py
```

## 📞 支持

如有问题请提交Issue或查看部署文档。

---

**⚡ 基于Vercel Serverless，免费部署，全球加速！**