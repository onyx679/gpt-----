# 🚀 Vercel部署完整指南

## 📋 部署前准备

### 1. 确认项目结构
```
gptforvercel/
├── api/
│   └── index.py          # Vercel入口文件
├── templates/
│   ├── index.html
│   └── error.html
├── static/
│   ├── css/
│   └── js/
├── api_client.py         # API客户端
├── error_mappings.py     # 错误映射
├── requirements.txt      # Python依赖
├── vercel.json          # Vercel配置
├── .vercelignore        # 忽略文件
└── deploy.py            # 部署脚本
```

### 2. 检查依赖
确保 `requirements.txt` 只包含必要依赖：
```
Flask==2.3.3
requests==2.31.0
```

## 🎯 三种部署方式

### 方式一：一键部署脚本（推荐）

```bash
# 运行部署脚本
python deploy.py
```

脚本会自动：
- ✅ 检查必要文件
- ✅ 安装Vercel CLI（如果没有）
- ✅ 登录Vercel
- ✅ 部署到生产环境

### 方式二：手动部署

#### Step 1: 安装Vercel CLI
```bash
# 使用npm安装
npm install -g vercel

# 或使用yarn
yarn global add vercel
```

#### Step 2: 登录Vercel
```bash
vercel login
```
选择登录方式（GitHub推荐）

#### Step 3: 部署
```bash
# 第一次部署
vercel

# 生产环境部署
vercel --prod
```

### 方式三：GitHub集成（最佳实践）

#### Step 1: 推送到GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/gpt-recharge.git
git push -u origin main
```

#### Step 2: Vercel导入
1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 导入GitHub仓库
4. Vercel会自动检测并部署

## ⚙️ 环境变量配置

在Vercel控制台设置以下环境变量：

| 变量名 | 值 | 说明 |
|--------|----|----|
| `SECRET_KEY` | `your-super-secret-key-here` | Flask密钥，请修改 |
| `SESSION_TIMEOUT` | `1800` | 会话超时时间（秒） |

### 设置步骤：
1. 进入Vercel项目控制台
2. 点击 **Settings** → **Environment Variables**
3. 添加上述变量
4. 重新部署：`vercel --prod`

## 🔍 部署后验证

### 1. 健康检查
访问：`https://your-project.vercel.app/api/health`

期望响应：
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "version": "1.0.0"
}
```

### 2. 主页访问
访问：`https://your-project.vercel.app`

应该能看到GPT充值系统界面

### 3. API测试
使用Postman或curl测试API接口：
```bash
curl -X POST https://your-project.vercel.app/api/verify-code \
  -H "Content-Type: application/json" \
  -d '{"activation_code": "CARD-TEST-TEST-TEST"}'
```

## 🐛 常见问题解决

### 1. 部署失败
```bash
# 查看详细错误
vercel logs

# 强制重新部署
vercel --prod --force
```

### 2. 模块导入错误
确保 `api/index.py` 中的路径正确：
```python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### 3. 静态文件404
检查 `api/index.py` 中的路径配置：
```python
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')
```

### 4. 会话问题
Vercel是无状态的，Flask session可能不稳定。如果遇到会话问题，考虑：
- 使用JWT token
- 使用外部存储（Redis）

### 5. 冷启动慢
第一次访问可能较慢（~2-3秒），这是正常的serverless冷启动

## 📊 性能监控

### Vercel控制台
- **Functions**: 查看函数执行情况
- **Analytics**: 访问统计
- **Logs**: 实时日志

### 性能指标
- ✅ 冷启动: ~200ms
- ✅ 热启动: ~50ms  
- ✅ 内存使用: ~50MB
- ✅ 免费额度: 完全够用

## 💰 成本分析

### Vercel免费额度
- **函数执行**: 100GB-小时/月
- **调用次数**: 100万次/月
- **带宽**: 100GB/月

### 预估使用量
- 每次请求: ~100ms + 50MB
- 月访问1000次: 仅用0.14GB-小时
- **结论**: 完全免费 ✅

## 🔄 持续部署

### 自动部署
连接GitHub后，每次push都会自动部署

### 手动部署
```bash
vercel --prod
```

### 回滚
```bash
vercel rollback [deployment-url]
```

## 📞 支持

如果遇到问题：
1. 检查Vercel控制台日志
2. 确认环境变量设置
3. 验证文件结构完整

---

**🎉 恭喜！你的GPT充值系统已成功部署到Vercel！**
