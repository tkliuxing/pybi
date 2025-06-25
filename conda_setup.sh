#!/bin/bash

echo "🚀 BI数据分析系统 - Conda环境设置"
echo

# 检查conda是否安装
if ! command -v conda &> /dev/null; then
    echo "❌ 未找到conda，请先安装Anaconda或Miniconda"
    echo "下载地址: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ 检测到conda环境"
echo

# 创建conda环境
echo "📦 创建conda环境 'pybi'..."
conda env create -f environment.yml
if [ $? -ne 0 ]; then
    echo "❌ 环境创建失败"
    exit 1
fi

echo
echo "✅ 环境创建成功！"
echo
echo "📋 后续步骤:"
echo "1. 激活环境: conda activate pybi"
echo "2. 启动系统: streamlit run app.py"
echo "3. 访问系统: http://localhost:8501"
echo
echo "或者直接运行: conda run -n pybi streamlit run app.py"
echo 