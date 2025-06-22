#!/usr/bin/env python3

import subprocess
import sys
import pathlib
import re
import json
import os
from datetime import datetime

# 检查bluetoothctl是否可用
def check_bluetoothctl():
    try:
        subprocess.run(["which", "bluetoothctl"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

# 检查蓝牙是否已启用
def is_bluetooth_enabled():
    try:
        result = subprocess.run(
            ["bluetoothctl", "show"],
            capture_output=True, text=True, check=True
        )
        return "Powered: yes" in result.stdout
    except subprocess.SubprocessError:
        return False

# 启用或禁用蓝牙
def toggle_bluetooth(enable=True):
    cmd = "power on" if enable else "power off"
    try:
        subprocess.run(["bluetoothctl", cmd], check=True)
        return True
    except subprocess.SubprocessError:
        return False

# 获取已配对设备列表
def get_paired_devices():
    try:
        result = subprocess.run(
            ["bluetoothctl", "paired-devices"],
            capture_output=True, text=True, check=True
        )
        
        devices = []
        for line in result.stdout.strip().split('\n'):
            if line:
                match = re.search(r'Device\s+([0-9A-F:]+)\s+(.*)', line)
                if match:
                    mac, name = match.groups()
                    devices.append((mac, name))
        return devices
    except subprocess.SubprocessError:
        return []

# 获取已连接设备列表
def get_connected_devices():
    try:
        result = subprocess.run(
            ["bluetoothctl", "devices"],
            capture_output=True, text=True, check=True
        )
        
        all_devices = []
        for line in result.stdout.strip().split('\n'):
            if line:
                match = re.search(r'Device\s+([0-9A-F:]+)\s+(.*)', line)
                if match:
                    mac, name = match.groups()
                    all_devices.append(mac)
                    
        connected_devices = []
        for mac in all_devices:
            info = subprocess.run(
                ["bluetoothctl", "info", mac],
                capture_output=True, text=True
            )
            if "Connected: yes" in info.stdout:
                match = re.search(r'Name:\s+(.*)', info.stdout)
                name = match.group(1) if match else "Unknown"
                
                # 尝试获取电量信息
                battery_level = get_device_battery(mac)
                
                connected_devices.append((mac, name, battery_level))
        
        return connected_devices
    except subprocess.SubprocessError:
        return []

# 获取设备电量
def get_device_battery(mac):
    try:
        # 使用upower获取电量信息（适用于大多数Linux系统）
        result = subprocess.run(
            ["upower", "-i", f"/org/freedesktop/UPower/devices/{mac.replace(':', '_')}"],
            capture_output=True, text=True
        )
        
        match = re.search(r'percentage:\s+(\d+)%', result.stdout)
        if match:
            return int(match.group(1))
            
        # 尝试bluetoothctl (部分设备可能支持)
        info = subprocess.run(
            ["bluetoothctl", "info", mac],
            capture_output=True, text=True
        )
        match = re.search(r'Battery Percentage:.*\((\d+)%\)', info.stdout)
        if match:
            return int(match.group(1))
            
        return None
    except:
        return None

# 扫描蓝牙设备
def scan_devices(timeout=5):
    devices = []
    try:
        # 开始扫描
        scan_proc = subprocess.Popen(
            ["bluetoothctl", "scan", "on"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待几秒
        try:
            subprocess.run(["sleep", str(timeout)], check=True)
        finally:
            # 停止扫描
            scan_proc.terminate()
            
        # 获取发现的设备
        result = subprocess.run(
            ["bluetoothctl", "devices"],
            capture_output=True, text=True, check=True
        )
        
        for line in result.stdout.strip().split('\n'):
            if line:
                match = re.search(r'Device\s+([0-9A-F:]+)\s+(.*)', line)
                if match:
                    mac, name = match.groups()
                    devices.append((mac, name))
                    
        return devices
    except subprocess.SubprocessError:
        return []

# 连接到设备
def connect_device(mac):
    try:
        subprocess.run(["bluetoothctl", "connect", mac], check=True)
        return True
    except subprocess.SubprocessError:
        return False

# 断开设备连接
def disconnect_device(mac):
    try:
        subprocess.run(["bluetoothctl", "disconnect", mac], check=True)
        return True
    except subprocess.SubprocessError:
        return False

# 显示设备电量图标
def get_battery_icon(level):
    if level is None:
        return ""
    
    if level > 80:
        return "󰁹 "
    elif level > 60:
        return "󰂀 "
    elif level > 40:
        return "󰁿 "
    elif level > 20:
        return "󰁾 "
    else:
        return "󰁻 "

# 主菜单定义
def get_main_menu():
    bt_enabled = is_bluetooth_enabled()
    
    menu = []
    if bt_enabled:
        menu.append(("󰂯  已连接设备", "connected_devices"))
        menu.append(("󰂯  扫描新设备", "scan_devices"))
        menu.append(("󰂲  断开所有设备", "disconnect_all"))
        menu.append(("󰂭  禁用蓝牙", "disable_bluetooth"))
    else:
        menu.append(("󰂯  启用蓝牙", "enable_bluetooth"))
    
    return menu

# 已连接设备菜单
def get_connected_devices_menu():
    devices = get_connected_devices()
    menu = []
    
    if not devices:
        menu.append(("没有已连接的设备", ""))
        menu.append(("返回", "main_menu"))
        return menu
        
    for mac, name, battery in devices:
        battery_str = f" {get_battery_icon(battery)}{battery}%" if battery is not None else ""
        menu.append((f"󰂱  {name}{battery_str} [已连接]", f"disconnect:{mac}"))
    
    menu.append(("返回", "main_menu"))
    return menu

# 扫描设备菜单
def get_scanned_devices_menu():
    # 显示扫描中提示
    show_notification("正在扫描蓝牙设备...")
    
    # 扫描设备
    devices = scan_devices()
    connected_macs = [mac for mac, _, _ in get_connected_devices()]
    menu = []
    
    if not devices:
        menu.append(("未发现设备", ""))
        menu.append(("返回", "main_menu"))
        return menu
    
    for mac, name in devices:
        if mac in connected_macs:
            menu.append((f"󰂱  {name} [已连接]", f"disconnect:{mac}"))
        else:
            menu.append((f"󰂯  {name}", f"connect:{mac}"))
    
    menu.append(("返回", "main_menu"))
    return menu

# 显示通知
def show_notification(message):
    try:
        subprocess.Popen(["notify-send", "蓝牙", message])
    except:
        pass

# 调用rofi显示菜单
def show_rofi_menu(options, prompt="蓝牙"):
    options_str = "\n".join(label for label, _ in options)
    
    rofi_cmd = [
        "rofi", "-dmenu", "-p", prompt,
        "-theme", str(pathlib.Path.home() / ".config/rofi/bluetooth.rasi")
    ]
    
    try:
        result = subprocess.run(
            rofi_cmd, 
            input=options_str, 
            text=True, 
            capture_output=True
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except subprocess.SubprocessError:
        return None

# 处理菜单选择
def handle_menu_action(choice, options):
    for label, action in options:
        if choice == label:
            return action
    return None

# 主程序
def main():
    if not check_bluetoothctl():
        show_notification("错误: 未找到bluetoothctl命令")
        sys.exit(1)
    
    current_menu = "main_menu"
    
    while True:
        if current_menu == "main_menu":
            options = get_main_menu()
        elif current_menu == "connected_devices":
            options = get_connected_devices_menu()
        elif current_menu == "scan_devices":
            options = get_scanned_devices_menu()
        else:
            break
        
        choice = show_rofi_menu(options)
        if choice is None:
            break
            
        action = handle_menu_action(choice, options)
        if action is None:
            break
            
        if action == "main_menu":
            current_menu = "main_menu"
        elif action == "connected_devices":
            current_menu = "connected_devices"
        elif action == "scan_devices":
            current_menu = "scan_devices"
        elif action == "enable_bluetooth":
            if toggle_bluetooth(True):
                show_notification("蓝牙已启用")
            else:
                show_notification("无法启用蓝牙")
            current_menu = "main_menu"
        elif action == "disable_bluetooth":
            if toggle_bluetooth(False):
                show_notification("蓝牙已禁用")
            else:
                show_notification("无法禁用蓝牙")
            break
        elif action == "disconnect_all":
            for mac, _, _ in get_connected_devices():
                disconnect_device(mac)
            show_notification("已断开所有设备")
            current_menu = "main_menu"
        elif action.startswith("connect:"):
            mac = action.split(":", 1)[1]
            if connect_device(mac):
                show_notification("设备连接成功")
            else:
                show_notification("无法连接到设备")
            current_menu = "connected_devices"
        elif action.startswith("disconnect:"):
            mac = action.split(":", 1)[1]
            if disconnect_device(mac):
                show_notification("设备已断开")
            else:
                show_notification("无法断开设备")
            current_menu = "connected_devices"
        else:
            break

if __name__ == "__main__":
    main()