"""
窗口标题查找工具
列出当前所有可见窗口的标题、类名、进程名，帮助你找到正确的 window_title 参数。
直接运行: python list_windows.py
"""
import win32gui
import win32process
import psutil


def get_process_name(hwnd):
    """通过窗口句柄获取进程名称"""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except Exception:
        return "N/A"


def list_windows():
    """枚举所有顶层可见窗口并打印信息"""
    windows = []

    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            process_name = get_process_name(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]

            if title.strip():  # 只保留有标题的窗口
                extra.append((hwnd, title, class_name, process_name, width,
                              height))
        return True

    win32gui.EnumWindows(callback, windows)

    # 按窗口标题排序
    windows.sort(key=lambda w: w[1])

    print("=" * 80)
    print("{:<40} {:<20} {:<8} {:<8}".format(
        "窗口标题", "进程名", "宽", "高"))
    print("=" * 80)

    for hwnd, title, class_name, process_name, width, height in windows:
        print("{:<40} {:<20} {:<8} {:<8}".format(
            title[:38], process_name[:18], width, height))

    print("=" * 80)
    print("共找到 {} 个可见窗口".format(len(windows)))
    print()
    print("提示: window_title 使用模糊匹配，只需包含窗口标题中的部分文字即可。")
    print("例如: 窗口标题为 'SD高达 v2.0 - goline.exe'，可传 'SD高达' 或 'goline.exe'")


def search_window(keyword):
    """按关键字搜索窗口"""
    print("搜索关键字: '{}'".format(keyword))
    print("-" * 60)

    found = []

    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            if keyword.lower() in title.lower() or keyword.lower(
            ) in class_name.lower():
                process_name = get_process_name(hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                extra.append((hwnd, title, class_name, process_name, width,
                              height))
        return True

    win32gui.EnumWindows(callback, found)

    if found:
        for hwnd, title, class_name, process_name, width, height in found:
            print("窗口标题: {}".format(title))
            print("窗口类名: {}".format(class_name))
            print("进程名:   {}".format(process_name))
            print("窗口句柄: {}".format(hwnd))
            print("窗口大小: {}x{}".format(width, height))
            print("-" * 60)
    else:
        print("未找到匹配窗口，请尝试其他关键字")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        search_window(sys.argv[1])
    else:
        list_windows()
        print()
        print("---")
        print("也可带关键字搜索: python list_windows.py 关键字")
