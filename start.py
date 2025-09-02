#!/usr/bin/env python3
"""
GPT充值系统启动脚本
支持开发和生产环境
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本检查通过: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """安装依赖包"""
    print("📦 正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False


def create_directories():
    """创建必要的目录"""
    directories = ["logs", "static/css", "static/js", "templates"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ 目录结构创建完成")


def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 创建必要目录
    create_directories()
    
    # 检查依赖文件
    if not os.path.exists("requirements.txt"):
        print("❌ 未找到requirements.txt文件")
        return False
    
    # 检查核心文件
    required_files = ["app.py", "api_client.py", "error_mappings.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 未找到核心文件: {file}")
            return False
    
    print("✅ 环境检查通过")
    return True


def run_development():
    """运行开发服务器"""
    print("🚀 启动开发服务器...")
    print("📍 服务地址: http://localhost:5000")
    print("💡 按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ 导入应用失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 服务运行错误: {e}")
        return False
    
    return True


def run_production():
    """运行生产服务器"""
    print("🚀 启动生产服务器...")
    
    # 检查是否安装了gunicorn
    try:
        import gunicorn
    except ImportError:
        print("❌ 未安装gunicorn，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gunicorn"])
    
    # 设置环境变量
    os.environ['FLASK_ENV'] = 'production'
    
    # 启动gunicorn
    cmd = [
        "gunicorn",
        "--bind", "0.0.0.0:5000",
        "--workers", "4",
        "--worker-class", "sync",
        "--timeout", "120",
        "--keepalive", "5",
        "--max-requests", "1000",
        "--max-requests-jitter", "100",
        "--access-logfile", "logs/access.log",
        "--error-logfile", "logs/error.log",
        "--log-level", "info",
        "app:app"
    ]
    
    try:
        print("📍 服务地址: http://localhost:5000")
        print("💡 按 Ctrl+C 停止服务")
        print("-" * 50)
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 生产服务器启动失败: {e}")
        return False
    
    return True


def show_status():
    """显示系统状态"""
    print("📊 系统状态")
    print("-" * 50)
    
    # Python版本
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    
    # 工作目录
    print(f"📁 工作目录: {os.getcwd()}")
    
    # 文件检查
    files = {
        "app.py": "主应用文件",
        "api_client.py": "API客户端",
        "error_mappings.py": "错误映射",
        "requirements.txt": "依赖文件",
        "templates/index.html": "主页模板"
    }
    
    print("\n📄 文件状态:")
    for file, desc in files.items():
        status = "✅" if os.path.exists(file) else "❌"
        print(f"  {status} {file} - {desc}")
    
    # 依赖包状态
    print("\n📦 依赖包状态:")
    try:
        import flask
        print(f"  ✅ Flask: {flask.__version__}")
    except ImportError:
        print("  ❌ Flask: 未安装")
    
    try:
        import requests
        print(f"  ✅ Requests: {requests.__version__}")
    except ImportError:
        print("  ❌ Requests: 未安装")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="GPT充值系统启动脚本")
    parser.add_argument("--mode", choices=["dev", "prod"], default="dev",
                       help="运行模式: dev(开发) 或 prod(生产)")
    parser.add_argument("--check", action="store_true",
                       help="检查环境状态")
    parser.add_argument("--install", action="store_true",
                       help="安装依赖包")
    parser.add_argument("--status", action="store_true",
                       help="显示系统状态")
    
    args = parser.parse_args()
    
    print("🎯 GPT充值系统 - Python版本")
    print("=" * 50)
    
    # 检查环境
    if args.check:
        return 0 if check_environment() else 1
    
    # 安装依赖
    if args.install:
        if not check_python_version():
            return 1
        return 0 if install_dependencies() else 1
    
    # 显示状态
    if args.status:
        show_status()
        return 0
    
    # 检查环境
    if not check_environment():
        print("\n💡 提示: 运行 'python start.py --install' 安装依赖")
        return 1
    
    # 运行服务器
    if args.mode == "dev":
        success = run_development()
    else:
        success = run_production()
    
    return 0 if success else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)


