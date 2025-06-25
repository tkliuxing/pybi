@echo off
chcp 65001 >nul
echo 🚀 启动BI数据分析系统...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 📦 检查依赖...
python -c "import streamlit, pandas, plotly, numpy" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  缺少依赖，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

REM 启动应用
echo 🌐 正在启动Web服务器...
echo 📱 请在浏览器中访问: http://localhost:8501
echo ⏹️  按 Ctrl+C 停止服务器
echo.
streamlit run app.py --server.port 8501 --server.address localhost

pause 