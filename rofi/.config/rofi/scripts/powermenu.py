#!/usr/bin/env python3
"""
使用 Rofi 实现的电源菜单脚本
"""

# 导入必要的库 
import subprocess

# 定义菜单选项
# 使用 Unicode 字符表示图标
# 确保你的 Rofi 主题支持这些图标
options = [
    " Lock",
    "⏾ Suspend",
    " Poweroff",
    " Reboot"
]

# 将选项转换为 Rofi 可接受的格式
# 每个选项占一行
menu = "\n".join(options)

# 调用 Rofi 显示菜单
# 使用 subprocess.run 执行 Rofi 命令
# -dmenu 选项表示使用 dmenu 风格的菜单
# -p 选项设置提示文本
# input 参数将菜单内容传递给 Rofi
rofi = subprocess.run(
    ["rofi", "-dmenu", "-p", "Power Menu"],
    input=menu.encode(),
    stdout=subprocess.PIPE
)

choice = rofi.stdout.decode().strip()

if choice == " Lock":
    subprocess.run(["hyprlock"])
elif choice == "⏾ Suspend":
    subprocess.run(["systemctl", "suspend"])
elif choice == " Poweroff":
    subprocess.run(["systemctl", "poweroff"])
elif choice == " Reboot":
    subprocess.run(["systemctl", "reboot"])
