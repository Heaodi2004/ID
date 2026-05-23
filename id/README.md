# 抖音链接解析器

一个简单易用的抖音视频链接解析工具，可以快速提取视频ID和用户ID。

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/Zc8N3C?referralCode=)

## 功能特点

- 🎵 支持多种抖音链接格式（短链接、长链接、笔记链接）
- 📝 支持混合文本输入，自动提取链接
- 🖥️ 美观的Web界面
- 📋 一键复制解析结果
- 🚀 自动打开浏览器
- 📦 支持打包成独立可执行文件
- ☁️ 一键部署到云端（支持Railway、Render、Vercel等）

## 快速开始

### 方式一：使用启动脚本（推荐）

#### Windows
双击运行 `start.bat`

#### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

### 方式二：手动启动

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 运行程序
```bash
python app.py
```

程序启动后会自动打开浏览器访问 http://127.0.0.1:5000

## 打包成可执行文件

### Windows
双击运行 `build.bat`

打包完成后，可执行文件位于 `dist/抖音链接解析器.exe`

### 其他平台
```bash
pip install pyinstaller
pyinstaller --clean build.spec
```

## 线上部署

想要让更多人使用？可以将项目部署到云端！

详细部署指南请查看 [DEPLOY.md](./DEPLOY.md)

### 快速部署（推荐）

点击下方按钮一键部署到 Railway：

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/Zc8N3C?referralCode=)

## 项目结构

```
id/
├── app.py                 # Flask主程序
├── wsgi.py               # WSGI入口（部署用）
├── douyin_parser.py       # 命令行版本
├── requirements.txt       # 依赖列表
├── Procfile              # 部署配置
├── runtime.txt           # Python版本
├── start.bat             # Windows启动脚本
├── start.sh              # Linux/Mac启动脚本
├── init-git.bat          # Git初始化脚本
├── build.bat             # Windows打包脚本
├── build.spec            # PyInstaller配置
├── .gitignore           # Git忽略文件
├── README.md             # 说明文档
├── DEPLOY.md             # 部署指南
└── templates/
    └── index.html        # 前端页面
```

## 使用说明

1. 启动程序后，浏览器会自动打开
2. 在输入框中粘贴抖音视频链接（可以包含其他文字）
3. 点击"解析链接"按钮
4. 查看解析结果，点击"复制"按钮复制需要的内容

## 支持的链接格式

- 短链接: `https://v.douyin.com/xxx`
- 长链接: `https://www.douyin.com/video/xxx`
- 笔记链接: `https://www.iesdouyin.com/share/note/xxx`

## 技术栈

- Python 3.7+
- Flask 2.0+
- Requests
- PyInstaller (打包用)

## 注意事项

- 首次运行需要联网安装依赖
- 部分链接可能因抖音反爬虫机制无法获取完整信息
- 请遵守抖音的使用条款，合理使用本工具

## 许可证

MIT License
