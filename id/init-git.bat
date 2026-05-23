@echo off
chcp 65001 >nul
echo ========================================
echo       初始化 Git 仓库
echo ========================================
echo.

echo [1/4] 检查 Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Git，请先安装 Git
    echo 下载地址: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo Git 检测成功
echo.

echo [2/4] 初始化仓库...
if exist .git (
    echo 仓库已存在，跳过初始化
) else (
    git init
    echo 仓库初始化完成
)
echo.

echo [3/4] 配置用户信息...
set /p email="请输入你的GitHub邮箱: "
set /p name="请输入你的GitHub用户名: "
git config user.email "%email%"
git config user.name "%name%"
echo 用户信息配置完成
echo.

echo [4/4] 首次提交...
git add .
git commit -m "初始化抖音链接解析器项目"
echo.
echo ========================================
echo  Git 仓库初始化完成！
echo ========================================
echo.
echo 下一步操作：
echo 1. 在 GitHub 上创建新仓库
echo 2. 运行以下命令推送代码：
echo.
echo git remote add origin https://github.com/你的用户名/仓库名.git
echo git branch -M main
echo git push -u origin main
echo.
pause
