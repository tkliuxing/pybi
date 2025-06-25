#!/usr/bin/env python3
"""
BI数据分析系统安装脚本
自动安装依赖和设置环境
"""

import subprocess
import sys
import os
import platform

def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("🚀 BI数据分析系统 - 安装程序")
    print("=" * 60)
    print()

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("   需要Python 3.8或更高版本")
        return False
    else:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True

def install_dependencies():
    """安装依赖包"""
    print("\n📦 安装依赖包...")
    
    # 升级pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✅ pip已升级")
    except subprocess.CalledProcessError:
        print("⚠️  pip升级失败，继续安装依赖...")
    
    # 安装依赖
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              check=True, capture_output=True, text=True)
        print("✅ 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        print("错误输出:", e.stderr)
        return False

def test_imports():
    """测试导入"""
    print("\n🧪 测试导入...")
    
    required_modules = ['streamlit', 'pandas', 'plotly', 'numpy']
    failed_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_modules.append(module)
    
    if failed_modules:
        print(f"\n❌ 以下模块导入失败: {', '.join(failed_modules)}")
        return False
    else:
        print("\n✅ 所有模块导入成功")
        return True

def create_directories():
    """创建必要的目录"""
    print("\n📁 创建目录...")
    
    directories = ['data', 'logs', 'exports']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ 创建目录: {directory}")
        else:
            print(f"ℹ️  目录已存在: {directory}")

def set_permissions():
    """设置文件权限（仅Linux/Mac）"""
    if platform.system() != "Windows":
        print("\n🔐 设置文件权限...")
        try:
            subprocess.run(["chmod", "+x", "start.sh"], check=True)
            subprocess.run(["chmod", "+x", "run.py"], check=True)
            print("✅ 文件权限设置成功")
        except subprocess.CalledProcessError:
            print("⚠️  文件权限设置失败")

def show_next_steps():
    """显示后续步骤"""
    print("\n" + "=" * 60)
    print("🎉 安装完成！")
    print("=" * 60)
    print()
    print("📋 后续步骤:")
    print("1. 启动系统:")
    if platform.system() == "Windows":
        print("   - 双击 start.bat 文件")
        print("   - 或在命令行运行: python run.py")
    else:
        print("   - 运行: ./start.sh")
        print("   - 或在命令行运行: python3 run.py")
    print()
    print("2. 访问系统:")
    print("   打开浏览器访问: http://localhost:8501")
    print()
    print("3. 使用示例数据:")
    print("   系统会自动生成示例数据，您也可以上传自己的CSV/Excel文件")
    print()
    print("📚 更多信息请查看 README.md 文件")
    print()

def main():
    """主函数"""
    print_banner()
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 测试导入
    if not test_imports():
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 设置权限
    set_permissions()
    
    # 显示后续步骤
    show_next_steps()

if __name__ == "__main__":
    main() 