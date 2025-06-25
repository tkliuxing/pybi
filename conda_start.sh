#!/bin/bash

echo "🚀 启动BI数据分析系统 (Conda环境)"
echo

# 检查conda环境是否存在
if ! conda env list | grep -q "pybi"; then
    echo "❌ 未找到conda环境 'pybi'"
    echo "请先运行 ./conda_setup.sh 创建环境"
    exit 1
fi

echo "✅ 检测到conda环境 'pybi'"
echo

# 启动应用
echo "🌐 正在启动Web服务器..."
echo "📱 请在浏览器中访问: http://localhost:8501"
echo "⏹️  按 Ctrl+C 停止服务器"
echo

conda run -n pybi streamlit run app.py --server.port 8501 --server.address localhost 