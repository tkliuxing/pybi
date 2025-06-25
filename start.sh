#!/bin/bash

echo "🚀 启动BI数据分析系统..."
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查依赖是否安装
echo "📦 检查依赖..."
python3 -c "import streamlit, pandas, plotly, numpy" &> /dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  缺少依赖，正在安装..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

# 启动应用
echo "🌐 正在启动Web服务器..."
echo "📱 请在浏览器中访问: http://localhost:8501"
echo "⏹️  按 Ctrl+C 停止服务器"
echo

streamlit run app.py --server.port 8501 --server.address localhost 