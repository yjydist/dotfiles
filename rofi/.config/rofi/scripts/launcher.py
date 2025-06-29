#!/usr/bin/env python3
"""
使用 Rofi 实现的启动器脚本
"""

import subprocess

theme = "./themes/Launcher.rasi"
mod = "drun"

def main():
    # 使用 subprocess.run 执行 rofi 命令
    # -show 参数指定显示的模式，这里使用 drun 模式
    # -theme 参数指定 Rofi 主题文件
    # -modi 参数指定模式
    rofi = subprocess.run(
        ["rofi", "-show", mod, "-theme", theme, "-modi", mod],
        stdout=subprocess.PIPE,
        text=True
    )
    
    # 获取用户选择的应用程序
    choice = rofi.stdout.strip()
    
    if choice:
        # 如果用户选择了应用程序，则执行该应用程序
        subprocess.run(choice.split())