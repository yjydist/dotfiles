#!/usr/bin/env python3
import subprocess, sys, pathlib

# —— 菜单定义：标题  → 对应命令 ——
MENU = [
    ("  Lock",      "swaylock -f -c 000000"),   # 字体请用 Nerd Font
    ("  Sleep",     "systemctl suspend"),
    ("  Shutdown",  "systemctl poweroff -i"),
    ("  Reboot",    "systemctl reboot"),
    ("󰍃  Logout",    "swaymsg exit"),
]

# —— 1. 生成选项字符串 ——
options = "\n".join(label for label, _ in MENU)

# —— 2. 调用 rofi-wayland ——
rofi_cmd = [
    "rofi", "-dmenu", "-p", "Power",            # dmenu 模式
    "-theme", str(pathlib.Path.home() / ".config/rofi/themes/PowerMenu.rasi")
]
result = subprocess.run(rofi_cmd, input=options, text=True, capture_output=True)
choice = result.stdout.strip()

# —— 3. 根据选择执行对应命令 ——
for label, cmd in MENU:
    if choice == label:
        subprocess.run(cmd, shell=True)
        sys.exit(0)
