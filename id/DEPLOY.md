# 抖音链接解析器 - 部署指南

本指南将帮助你将抖音链接解析器部署到GitHub并在线上运行，让更多人可以使用！

## 目录

1. [准备工作](#准备工作)
2. [推送到GitHub](#推送到github)
3. [免费部署方案](#免费部署方案)
   - [方案一：Railway（推荐）](#方案一railway推荐)
   - [方案二：Render](#方案二render)
   - [方案三：Vercel](#方案三vercel)
   - [方案四：Heroku](#方案四heroku)

---

## 准备工作

### 1. 创建GitHub账号

如果你还没有GitHub账号，请先访问 https://github.com 注册一个。

### 2. 安装Git

#### Windows
下载并安装 Git for Windows: https://git-scm.com/download/win

#### Mac
```bash
brew install git
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install git
```

---

## 推送到GitHub

### 第一步：初始化Git仓库

在项目文件夹中打开命令行（PowerShell/终端），执行以下命令：

```bash
# 初始化Git仓库
git init

# 配置用户信息（替换为你的GitHub邮箱和用户名）
git config user.email "你的邮箱@example.com"
git config user.name "你的GitHub用户名"
```

### 第二步：添加文件并提交

```bash
# 添加所有文件
git add .

# 提交更改
git commit -m "初始化抖音链接解析器项目"
```

### 第三步：在GitHub上创建仓库

1. 访问 https://github.com/new
2. 填写仓库名称（例如：douyin-parser）
3. 选择 Public（公开）或 Private（私有）
4. **不要**勾选 "Initialize this repository with a README"
5. 点击 "Create repository"

### 第四步：推送到GitHub

```bash
# 关联远程仓库（替换为你的GitHub用户名和仓库名）
git remote add origin https://github.com/你的用户名/douyin-parser.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

如果提示需要认证，请按照提示使用GitHub账号登录或使用Personal Access Token。

---

## 免费部署方案

### 方案一：Railway（推荐 ⭐⭐⭐⭐⭐）

Railway 提供免费的部署额度，非常适合个人项目！

#### 部署步骤：

1. 访问 https://railway.app 并使用GitHub账号登录
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择你刚才推送的仓库
4. 点击 "Deploy Now"
5. 等待部署完成（通常1-2分钟）
6. 部署完成后，点击 "Settings" → "Generate Domain" 生成访问地址
7. 完成！你现在有了一个可以公开访问的链接

#### 优势：
- ✅ 完全免费（有一定额度限制）
- ✅ 部署速度快
- ✅ 自动HTTPS
- ✅ 支持自定义域名

---

### 方案二：Render

Render 也是一个很好的免费部署平台。

#### 部署步骤：

1. 访问 https://render.com 并使用GitHub账号登录
2. 点击 "New" → "Web Service"
3. 选择你的仓库
4. 配置部署设置：
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`
5. 点击 "Create Web Service"
6. 等待部署完成

#### 优势：
- ✅ 免费额度充足
- ✅ 支持自定义域名
- ✅ 自动部署

---

### 方案三：Vercel

Vercel 主要面向前端项目，但也可以部署Flask应用。

#### 部署步骤：

1. 访问 https://vercel.com 并使用GitHub账号登录
2. 点击 "New Project" → 选择你的仓库
3. 点击 "Deploy"
4. 需要额外配置 vercel.json 文件（见下文）

#### 创建 vercel.json：

在项目根目录创建 `vercel.json` 文件：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "wsgi.py"
    }
  ]
}
```

然后推送到GitHub，Vercel会自动重新部署。

---

### 方案四：Heroku

Heroku 是老牌的PaaS平台，仍然可以使用。

#### 部署步骤：

1. 访问 https://heroku.com 注册账号
2. 安装 Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
3. 登录 Heroku:
```bash
heroku login
```
4. 创建应用:
```bash
heroku create 你的应用名称
```
5. 推送代码:
```bash
git push heroku main
```
6. 打开应用:
```bash
heroku open
```

---

## 项目文件说明

部署所需的关键文件：

| 文件 | 说明 |
|------|------|
| `requirements.txt` | Python依赖列表 |
| `Procfile` | Heroku/Railway启动配置 |
| `runtime.txt` | Python版本指定 |
| `wsgi.py` | WSGI入口文件 |
| `.gitignore` | Git忽略文件 |

---

## 常见问题

### Q: 部署后无法访问？
A: 检查一下：
1. 确保 `requirements.txt` 包含了所有依赖
2. 确保启动命令正确使用了 `gunicorn`
3. 检查平台的日志查看错误信息

### Q: 如何更新代码？
A: 很简单：
1. 本地修改代码
2. 提交并推送到GitHub
3. 部署平台会自动重新部署

### Q: 可以自定义域名吗？
A: 可以！大部分平台都支持自定义域名，在设置中添加即可。

### Q: 免费版有什么限制？
A: 
- Railway: 每月500小时运行时间，$5.00额度
- Render: 每月750小时运行时间
- Vercel: 每月100GB带宽，无限运行时间
- Heroku: 每月550小时运行时间（需绑定信用卡）

---

## 下一步

部署成功后，你可以：
- 📢 分享链接给朋友使用
- 🌟 在GitHub仓库添加README和Star
- 💾 定期更新代码和功能
- 🎨 美化界面

祝你使用愉快！🎉
