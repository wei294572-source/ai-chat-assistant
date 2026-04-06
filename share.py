"""
创建公网分享链接
使用 cloudflare tunnel (cloudflared)
"""
import subprocess
import sys
import time
import requests

def create_tunnel():
    """使用 cloudflare 创建隧道"""
    try:
        # 尝试启动 cloudflared
        result = subprocess.run(
            ["npx", "-y", "cloudflare-tunnel", "--port", "8502"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if "https://" in result.stdout:
            for line in result.stdout.split('\n'):
                if "https://" in line:
                    print(f"\n✅ 公网访问链接: {line.strip()}")
                    return True

    except Exception as e:
        print(f"错误: {e}")

    print("\n请尝试以下手动方案:")
    print("1. 访问 https://localtunnel.me/")
    print("2. 输入端口: 8502")
    print("3. 获取生成的链接分享给其他人")
    return False

if __name__ == "__main__":
    print("正在创建公网隧道...")
    create_tunnel()
