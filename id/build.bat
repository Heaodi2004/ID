@echo off
chcp 65001 >nul
echo ========================================
echo       抖音链接解析器 - 打包脚本
echo ========================================
echo.

echo [1/4] 检查 PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo 错误: PyInstaller 安装失败
        pause
        exit /b 1
    )
)
echo PyInstaller 准备就绪
echo.

echo [2/4] 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo 清理完成
echo.

echo [3/4] 开始打包...
pyinstaller --clean build.spec
if errorlevel 1 (
    echo 错误: 打包失败
    pause
    exit /b 1
)
echo 打包完成
echo.

echo [4/4] 打包成功！
echo.
echo ========================================
echo  可执行文件位置: dist\抖音链接解析器.exe
echo ========================================
echo.

pause
