#!/usr/bin/env python3
"""
使用 Rofi 实现的播放器菜单脚本
"""

import subprocess

def get_player_status():
    """获取当前播放器状态"""
    try:
        output = subprocess.check_output(["playerctl", "status"]).decode().strip()
        return output
    except subprocess.CalledProcessError:
        return "Stopped"