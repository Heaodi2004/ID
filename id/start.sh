#!/bin/bash

echo "========================================"
echo "      抖音链接解析器 - 启动脚本"
echo "========================================"
echo ""

echo "[1/3] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "错误: 未找到 Python，请先安装 Python"
        exit 1
    fi
    PYTHON_CMD=python
else
    PYTHON_CMD=python3
fi
$PYTHON_CMD --version
echo "Python 检测成功"
echo ""

echo "[2/3] 检查依赖包..."
if ! $PYTHON_CMD -c "import flask" 2>/dev/null; then
    echo "正在安装依赖包..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi
echo "依赖检查完成"
echo ""

echo "[3/3] 启动服务..."
echo ""
echo "========================================"
echo " 服务已启动！"
echo " 请在浏览器中打开: http://127.0.0.1:5000"
echo " 按 Ctrl+C 停止服务"
echo "========================================"
echo ""

$PYTHON_CMD app.py
