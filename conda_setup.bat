@echo off
chcp 65001 >nul
echo 🚀 BI数据分析系统 - Conda环境设置
echo.

REM 检查conda是否安装
conda --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到conda，请先安装Anaconda或Miniconda
    echo 下载地址: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo ✅ 检测到conda环境
echo.

REM 创建conda环境
echo 📦 创建conda环境 'pybi'...
conda env create -f environment.yml
if errorlevel 1 (
    echo ❌ 环境创建失败
    pause
    exit /b 1
)

echo.
echo ✅ 环境创建成功！
echo.
echo 📋 后续步骤:
echo 1. 激活环境: conda activate pybi
echo 2. 启动系统: streamlit run app.py
echo 3. 访问系统: http://localhost:8501
echo.
echo 或者直接运行: conda run -n pybi streamlit run app.py
echo.

pause 