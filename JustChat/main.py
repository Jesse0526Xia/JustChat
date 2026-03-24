"""
虚拟恋人应用启动脚本
"""

import argparse
import signal
import sys
import threading

from src.app import app, initialize, managers


def signal_handler(sig, frame):
    """信号处理函数"""
    print("\n正在关闭应用...")

    # 关闭微信连接
    if 'wechat' in managers and managers['wechat'].is_logged_in:
        managers['wechat'].logout()

    # 关闭数据库连接
    if 'database' in managers:
        managers['database'].disconnect()

    sys.exit(0)


def start_wechat():
    """启动微信监听"""
    print("启动微信监听...")
    managers['wechat'].login(enable_qr=True)
    managers['wechat'].run()


def main():
    """主函数"""
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)

    # 初始化应用
    initialize()

    # 解析命令行参数
    parser = argparse.ArgumentParser(description="虚拟恋人应用")
    parser.add_argument('--web', action='store_true', help='启动Web服务器')
    parser.add_argument('--wechat', action='store_true', help='启动微信监听')
    parser.add_argument('--all', action='store_true', help='同时启动Web和微信')
    args = parser.parse_args()

    if args.all or (args.web and args.wechat):
        # 同时启动Web和微信
        print("同时启动Web服务器和微信监听...")
        wechat_thread = threading.Thread(target=start_wechat, daemon=True)
        wechat_thread.start()
        app.run(host='0.0.0.0', port=5000, use_reloader=False)

    elif args.web:
        # 仅启动Web服务器
        print("启动Web服务器...")
        app.run(host='0.0.0.0', port=5000)

    elif args.wechat:
        # 仅启动微信监听
        start_wechat()

    else:
        # 默认启动Web服务器
        print("启动Web服务器...")
        app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
