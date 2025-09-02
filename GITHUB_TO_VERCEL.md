# 🚀 GitHub到Vercel完整部署指南

## 📋 最终项目结构

清理后的项目只包含必要文件：

```
gptforvercel/
├── api/
│   └── index.py          # ✅ Vercel入口文件
├── templates/            # ✅ HTML模板
│   ├── index.html
│   └── error.html  
├── static/              # ✅ 静态资源
│   ├── css/
│   └── js/
├── api_client.py        # ✅ API客户端
├── error_mappings.py    # ✅ 错误处理
├── requirements.txt     # ✅ Python依赖
├── vercel.json         # ✅ Vercel配置
├── .gitignore          # ✅ Git忽略文件
└── README.md           # ✅ 项目说明
```

## 🔥 **第一步：创建GitHub仓库**

### 1.1 在GitHub上创建新仓库
1. 访问 https://github.com
2. 登录你的账户
3. 点击右上角 "+" → "New repository"
4. 仓库名：`gpt-recharge` (或你喜欢的名字)
5. 设为 **Public** (Vercel免费版需要公开仓库)
6. ✅ 勾选 "Add a README file"
7. 点击 "Create repository"

### 1.2 获取仓库地址
创建后你会得到类似这样的地址：
```
https://github.com/你的用户名/gpt-recharge.git
```

## 🚀 **第二步：上传项目到GitHub**

### 2.1 初始化Git仓库
在你的项目目录执行：
```bash
git init
git add .
git commit -m "Initial commit: GPT recharge system"
```

### 2.2 连接远程仓库
```bash
git remote add origin https://github.com/你的用户名/gpt-recharge.git
git branch -M main
git push -u origin main
```

## ⚡ **第三步：Vercel一键部署**

### 3.1 访问Vercel
1. 打开 https://vercel.com
2. 点击 "Sign Up" 注册账户
3. **选择 "Continue with GitHub"** (推荐)
4. 授权Vercel访问你的GitHub

### 3.2 导入项目
1. 登录后点击 "New Project"
2. 在 "Import Git Repository" 中找到你的 `gpt-recharge` 仓库
3. 点击 "Import"

### 3.3 配置项目
Vercel会自动检测到这是Python项目：
- **Framework Preset**: 会自动选择 "Other"
- **Root Directory**: 保持 "./" 
- **Build Command**: 留空
- **Output Directory**: 留空
- **Install Command**: 保持默认

点击 **"Deploy"**

## 🔧 **第四步：设置环境变量**

部署完成后，需要设置环境变量：

### 4.1 进入项目设置
1. 在Vercel控制台找到你的项目
2. 点击项目名进入详情页
3. 点击顶部 **"Settings"** 标签
4. 在左侧菜单点击 **"Environment Variables"**

### 4.2 添加必需变量
添加以下环境变量：

| Name | Value | Environment |
|------|-------|-------------|
| `SECRET_KEY` | `your-super-secret-key-here-change-this` | Production |
| `SESSION_TIMEOUT` | `1800` | Production |

**注意**: `SECRET_KEY` 请设置为一个复杂的随机字符串！

### 4.3 重新部署
设置环境变量后：
1. 回到 **"Deployments"** 标签
2. 点击最新部署右侧的 "..." 菜单
3. 选择 **"Redeploy"**
4. 等待重新部署完成

## 🎉 **第五步：测试部署**

### 5.1 访问你的应用
部署成功后，Vercel会提供一个域名，类似：
```
https://gpt-recharge-你的用户名.vercel.app
```

### 5.2 功能测试
1. **主页测试**: 访问根域名，应该看到GPT充值界面
2. **健康检查**: 访问 `/api/health`，应该返回JSON状态
3. **API测试**: 尝试输入激活码验证功能

### 5.3 查看日志
如果有问题，在Vercel控制台：
1. 进入项目详情
2. 点击 **"Functions"** 标签
3. 点击 **"View Function Logs"** 查看详细日志

## 🔄 **更新部署**

以后要更新代码：
```bash
git add .
git commit -m "更新描述"
git push origin main
```

Vercel会自动检测到GitHub更新并重新部署！

## 🌟 **自定义域名（可选）**

如果你有自己的域名：
1. 在Vercel项目设置中点击 **"Domains"**
2. 添加你的域名
3. 按照提示配置DNS记录

## 🐛 **常见问题**

### 问题1: 部署失败
- 检查 `vercel.json` 配置是否正确
- 确保 `requirements.txt` 只包含必要依赖

### 问题2: 页面404
- 确保 `api/index.py` 存在
- 检查路径配置是否正确

### 问题3: 静态文件加载失败
- 确保 `templates/` 和 `static/` 目录存在
- 检查 Flask 配置中的路径

### 问题4: 环境变量不生效
- 确保在 Production 环境设置变量
- 设置后需要重新部署

## 📊 **成本说明**

Vercel免费额度：
- ✅ **100GB-小时/月** 函数执行时间
- ✅ **100万次/月** 函数调用
- ✅ **100GB/月** 带宽

你的应用预计使用量：
- 每次请求约100ms，50MB内存
- 月访问1000次仅用0.14GB-小时
- **完全在免费额度内！** 🎉

---

**🎯 按照这个指南，你的GPT充值系统就能完美运行在Vercel上了！**
