@echo off
chcp 65001 >nul
echo 🚀 启动BI数据分析系统 (Conda环境)
echo.

REM 检查conda环境是否存在
conda env list | findstr "pybi" >nul
if errorlevel 1 (
    echo ❌ 未找到conda环境 'pybi'
    echo 请先运行 conda_setup.bat 创建环境
    pause
    exit /b 1
)

echo ✅ 检测到conda环境 'pybi'
echo.

REM 启动应用
echo 🌐 正在启动Web服务器...
echo 📱 请在浏览器中访问: http://localhost:8501
echo ⏹️  按 Ctrl+C 停止服务器
echo.

conda run -n pybi streamlit run app.py --server.port 8501 --server.address localhost

pause 