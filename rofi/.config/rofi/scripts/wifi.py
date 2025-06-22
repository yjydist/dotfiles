#!/usr/bin/env python3

import subprocess, sys, pathlib

def scan_wifi_networks():
    """扫描并返回可用的WiFi网络列表"""
    try:
        # 使用nmcli扫描WiFi网络
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "device", "wifi", "list"],
            capture_output=True, text=True, check=True
        )
        networks = []
        
        # 解析输出
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(':')
                if len(parts) >= 3:
                    ssid, signal, security = parts[0], parts[1], parts[2]
                    # 如果有安全性，添加一个锁图标
                    security_icon = "🔒 " if security and security != "--" else ""
                    # 添加信号强度图标
                    signal_int = int(signal) if signal.isdigit() else 0
                    if signal_int > 80:
                        signal_icon = "󰤨"
                    elif signal_int > 60:
                        signal_icon = "󰤥"
                    elif signal_int > 40:
                        signal_icon = "󰤢"
                    elif signal_int > 20:
                        signal_icon = "󰤟"
                    else:
                        signal_icon = "󰤯"
                    
                    network = f"{signal_icon} {security_icon}{ssid} ({signal}%)"
                    networks.append((network, f"nmcli device wifi connect '{ssid}'"))
        
        return networks
    except subprocess.SubprocessError:
        return [("Error scanning networks", "")]

# —— 菜单定义：标题  → 对应命令 ——
MENU = [
    ("  Connect", "rofi-wifi-menu"),
    ("󰤨  Disconnect", "nmcli device disconnect wlan0"),
    ("󰤨  Enable Wi-Fi", "nmcli radio wifi on"),
    ("󰤨  Disable Wi-Fi", "nmcli radio wifi off"),
    ("  Scan Networks", ""),  # 这个选项会触发网络扫描
]

# —— 1. 生成选项字符串 ——
options = "\n".join(label for label, _ in MENU)
# —— 2. 调用 rofi-wayland ——
rofi_cmd = [
    "rofi", "-dmenu", "-p", "Wi-Fi",            # dmenu 模式
    "-theme", str(pathlib.Path.home() / ".config/rofi/wifi.rasi")
]
result = subprocess.run(rofi_cmd, input=options, text=True, capture_output=True)
choice = result.stdout.strip()

# —— 3. 根据选择执行对应命令 ——
# 处理"扫描网络"选项
if choice == "  Scan Networks":
    # 扫描网络
    networks = scan_wifi_networks()
    if not networks:
        sys.exit(0)
    
    # 构建网络列表选项
    network_options = "\n".join(label for label, _ in networks)
    
    # 显示网络列表
    result = subprocess.run(
        rofi_cmd, 
        input=network_options, 
        text=True, 
        capture_output=True
    )
    network_choice = result.stdout.strip()
    
    # 执行选择的网络连接命令
    for label, cmd in networks:
        if network_choice == label and cmd:
            subprocess.run(cmd, shell=True)
            break
    
    sys.exit(0)
else:
    # 处理原有菜单选项
    for label, cmd in MENU:
        if choice == label:
            subprocess.run(cmd, shell=True)
            sys.exit(0)

# 如果没有选择任何项，则退出脚本
sys.exit(0)
