@echo off
chcp 65001 >nul
echo ========================================
echo       抖音链接解析器 - 启动脚本
echo ========================================
echo.

echo [1/3] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python
    pause
    exit /b 1
)
echo Python 检测成功
echo.

echo [2/3] 检查依赖包...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)
echo 依赖检查完成
echo.

echo [3/3] 启动服务...
echo.
echo ========================================
echo  服务已启动！
echo  请在浏览器中打开: http://127.0.0.1:5000
echo  按 Ctrl+C 停止服务
echo ========================================
echo.

python app.py

pause
