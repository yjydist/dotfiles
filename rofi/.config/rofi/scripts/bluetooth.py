#!/usr/bin/env python3
"""
使用 Rofi 实现的电源菜单脚本
"""

import subprocess

# 列出设备
# 使用 subprocess.check_output 执行 bluetoothctl 命令获取设备列表
# decode() 将字节转换为字符串
devices_raw = subprocess.check_output(["bluetoothctl", "devices"]).decode()

# 解析设备列表
# 将设备信息按行分割，并提取 MAC 地址和设备名称
devices = []

# 遍历每一行设备信息
# 使用 split() 方法分割字符串，提取 MAC 地址和设备名称
# 如果行包含至少三个部分（MAC 地址、设备名称和其他信息），则将其添加到 devices 列表中
# 最终生成的 devices 列表将包含格式为 "MAC 地址 设备名称" 的字符串
for line in devices_raw.strip().split("\n"):
    parts = line.split(" ", 2)
    if len(parts) >= 3:
        devices.append(f"{parts[1]} {parts[2]}")

menu = "\n".join(devices)
rofi = subprocess.run(
    ["rofi", "-dmenu", "-p", "Bluetooth"],
    input=menu.encode(),
    stdout=subprocess.PIPE
)

choice = rofi.stdout.decode().strip()
if choice:
    mac = choice.split()[0]
    subprocess.run(["bluetoothctl", "connect", mac])
