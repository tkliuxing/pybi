#!/usr/bin/env python3
"""
BI数据分析系统启动脚本
"""

import subprocess
import sys
import os

def check_dependencies():
    """检查依赖是否已安装"""
    try:
        import streamlit
        import pandas
        import plotly
        import numpy
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def main():
    """主函数"""
    print("🚀 启动BI数据分析系统...")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查app.py是否存在
    if not os.path.exists('app.py'):
        print("❌ 找不到app.py文件")
        sys.exit(1)
    
    # 启动Streamlit应用
    try:
        print("🌐 正在启动Web服务器...")
        print("📱 请在浏览器中访问: http://localhost:8501")
        print("⏹️  按 Ctrl+C 停止服务器")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 