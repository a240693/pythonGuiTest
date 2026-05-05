import json
import os
import subprocess
import sys
from datetime import datetime

import easygui as gui

HISTORY_FILE = "allGui_history.json"

# 所有GUI脚本汇总
# 选择项 -> 对应文件名
gui_map = {
    "碧蓝档案": "blueAirGui.py",
    "尘白禁区": "cbjqGui.py",
    "龙珠激战传说": "dblAirGui.py",
    "FGO": "fgoGui.py",
    "访客换防": "guestGui.py",
    "星轨": "honkaiTrainGui.py",
    "坎公Air": "kgAirGui.py",
    "综合脚本(方舟/PCR/坎公)": "mainGui.py",
    "PCR Air": "pcrAirGui.py",
    "SD高达G世纪": "sdGundamGui.py",
    "特殊脚本(坎公精简)": "SpjjGui.py",
    "PCR换防": "starGui.py",
    "JJC击剑": "starJJCGui.py",
}

choices = tuple(gui_map.keys()) + ("关闭",)

# 运行中的子进程追踪: {脚本名: Popen对象}
running_processes = {}


def load_history():
    """加载历史选择记录"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_history(history):
    """保存历史选择记录"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def format_history_msg(history):
    """将历史记录格式化为显示文本"""
    if not history:
        return "暂无选择记录"
    lines = ["上次选择时间："]
    sorted_items = sorted(history.items(), key=lambda x: x[1], reverse=True)
    for name, ts in sorted_items:
        lines.append(f"  {name}: {ts}")
    return "\n".join(lines)


def cleanup_dead():
    """清理已退出的子进程记录"""
    for name in list(running_processes.keys()):
        proc = running_processes[name]
        if proc.poll() is not None:
            del running_processes[name]


def format_running_msg():
    """格式化运行中进程的显示文本"""
    cleanup_dead()
    if not running_processes:
        return ""
    lines = ["", "当前运行中的脚本：" if len(running_processes) == 1 else "当前运行中的脚本："]
    for name in running_processes:
        lines.append(f"  ● {name}")
    return "\n".join(lines)


def kill_process(name):
    """终止指定子进程"""
    proc = running_processes.get(name)
    if proc and proc.poll() is None:
        proc.kill()
        proc.wait()
        del running_processes[name]


if __name__ == "__main__":
    history = load_history()
    # CREATE_NEW_CONSOLE = 0x00000010, CREATE_NEW_PROCESS_GROUP = 0x00000200
    CREATE_NEW_CONSOLE = 0x00000010
    CREATE_NEW_PROCESS_GROUP = 0x00000200

    while True:
        cleanup_dead()
        # 构建动态选项：运行中的脚本追加"终止"选项
        dynamic_choices = list(choices)
        kill_options = []
        for name in running_processes:
            kill_label = f"终止: {name}"
            kill_options.append(kill_label)
        if kill_options:
            dynamic_choices = kill_options + ["========"] + dynamic_choices

        msg = format_history_msg(history) + format_running_msg()
        choice = gui.choicebox("脚本总菜单", msg, choices=tuple(dynamic_choices))
        if choice is None or choice == "关闭":
            break

        # 处理终止命令
        if choice and choice.startswith("终止: "):
            target_name = choice[4:]  # 去掉前缀 "终止: "
            kill_process(target_name)
            gui.msgbox(f"已终止: {target_name}", "操作完成")
            continue

        script = gui_map.get(choice)
        if script:
            # 已在运行中，防呆确认
            if choice in running_processes:
                confirm = gui.ccbox(
                    f"【{choice}】正在运行中！\n\n确定要重新启动吗？\n（会先终止旧进程再启动新进程）",
                    "防呆确认",
                    choices=("重新启动", "取消"),
                )
                if not confirm:
                    continue
                kill_process(choice)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history[choice] = now
            save_history(history)

            # 启动子进程：独立控制台窗口（日志可见），新进程组（脱钩）
            proc = subprocess.Popen(
                [sys.executable, script],
                creationflags=CREATE_NEW_CONSOLE | CREATE_NEW_PROCESS_GROUP,
            )
            running_processes[choice] = proc
