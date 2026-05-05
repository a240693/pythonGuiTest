import json
import os
import subprocess
import sys
import tkinter as tk
from datetime import datetime
from tkinter import font as tkfont

HISTORY_FILE = "allGui_history.json"

gui_list = [
    ("碧蓝档案", "blueAirGui.py"),
    ("尘白禁区", "cbjqGui.py"),
    ("龙珠激战传说", "dblAirGui.py"),
    ("FGO", "fgoGui.py"),
    ("访客换防", "guestGui.py"),
    ("星轨", "honkaiTrainGui.py"),
    ("坎公Air", "kgAirGui.py"),
    ("综合脚本(方舟/PCR/坎公)", "mainGui.py"),
    ("PCR Air", "pcrAirGui.py"),
    ("SD高达G世纪", "sdGundamGui.py"),
    ("特殊脚本(坎公精简)", "SpjjGui.py"),
    ("PCR换防", "starGui.py"),
    ("JJC击剑", "starJJCGui.py"),
]

running_processes = {}
CREATE_NEW_CONSOLE = 0x00000010
CREATE_NEW_PROCESS_GROUP = 0x00000200
POLL_INTERVAL_MS = 2000

# ── 配色（与 storage_manager.html 一致） ──
C = {
    "bg_dark": "#0a0c14",
    "bg_card": "#111627",
    "bg_card_hover": "#151b33",
    "bg_header": "#0f121f",
    "bg_input": "#0d1020",
    "border": "#1a2350",
    "border_glow": "#00e5ff",
    "border_glow_dim": "#003344",
    "text": "#c8d6e5",
    "text_dim": "#7889a8",
    "accent": "#00e5ff",
    "accent_dim": "#0a1a22",
    "warning": "#ffb74d",
    "danger": "#ff5370",
    "success": "#69f0ae",
    "running": "#00e676",
    "idle": "#4a5568",
}

FONT_MONO = ("Consolas", 10)
FONT_MONO_SM = ("Consolas", 9)
FONT_TITLE = ("Consolas", 14, "bold")
FONT_STATUS = ("Consolas", 9)
FONT_UI = ("Microsoft YaHei", 9)


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_history(h):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(h, f, ensure_ascii=False, indent=2)


def launch_script(name, script):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history[name] = now
    save_history(history)
    proc = subprocess.Popen(
        [sys.executable, script],
        creationflags=CREATE_NEW_CONSOLE | CREATE_NEW_PROCESS_GROUP,
    )
    running_processes[name] = proc


def kill_script(name):
    proc = running_processes.get(name)
    if proc and proc.poll() is None:
        proc.kill()
        proc.wait()
        del running_processes[name]
        return True
    return False


def is_running(name):
    proc = running_processes.get(name)
    if proc is None:
        return False
    if proc.poll() is not None:
        running_processes.pop(name, None)
        return False
    return True


def cleanup_dead():
    for name in list(running_processes.keys()):
        proc = running_processes.get(name)
        if proc and proc.poll() is not None:
            del running_processes[name]


# ── 确认对话框 ──
def ask_confirm(title, message):
    """自定义暗色确认弹窗"""
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.configure(bg=C["bg_card"])
    dialog.resizable(False, False)
    dialog.transient()

    w, h = 380, 150
    x = dialog.winfo_screenwidth() // 2 - w // 2
    y = dialog.winfo_screenheight() // 2 - h // 2
    dialog.geometry(f"{w}x{h}+{x}+{y}")

    # 边框发光
    dialog.overrideredirect(True)
    border_frame = tk.Frame(dialog, bg=C["border_glow"], padx=1, pady=1)
    border_frame.pack(fill=tk.BOTH, expand=True)
    inner = tk.Frame(border_frame, bg=C["bg_card"])
    inner.pack(fill=tk.BOTH, expand=True)

    # 标题栏（可拖拽）
    title_bar = tk.Frame(inner, bg=C["bg_header"], height=32)
    title_bar.pack(fill=tk.X)
    tk.Label(title_bar, text=f"  {title}", bg=C["bg_header"], fg=C["accent"],
             font=FONT_MONO_SM, anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=True)

    # 内容
    msg_frame = tk.Frame(inner, bg=C["bg_card"], padx=24, pady=16)
    msg_frame.pack(fill=tk.BOTH, expand=True)
    tk.Label(msg_frame, text=message, bg=C["bg_card"], fg=C["text"],
             font=FONT_UI, justify=tk.LEFT, wraplength=330).pack()

    # 按钮
    btn_frame = tk.Frame(inner, bg=C["bg_header"], height=44)
    btn_frame.pack(fill=tk.X)
    result = tk.BooleanVar(value=False)

    def on_yes():
        result.set(True)
        dialog.destroy()

    def on_no():
        result.set(False)
        dialog.destroy()

    btn_yes = tk.Button(btn_frame, text="确认", command=on_yes,
                        bg=C["accent_dim"], fg=C["accent"], font=FONT_MONO_SM,
                        activebackground="#002233", activeforeground=C["accent"],
                        relief=tk.FLAT, cursor="hand2", padx=20, pady=2,
                        borderwidth=1, highlightthickness=0)
    btn_no = tk.Button(btn_frame, text="取消", command=on_no,
                       bg=C["bg_card"], fg=C["text_dim"], font=FONT_MONO_SM,
                       activebackground=C["bg_card_hover"], activeforeground=C["text"],
                       relief=tk.FLAT, cursor="hand2", padx=20, pady=2,
                       borderwidth=1, highlightthickness=0)
    # 右侧布局
    btn_frame_right = tk.Frame(btn_frame, bg=C["bg_header"])
    btn_frame_right.pack(side=tk.RIGHT, padx=12)
    btn_yes.pack(side=tk.RIGHT, padx=(8, 0))
    btn_no.pack(side=tk.RIGHT)

    # 关闭按钮（X）
    close_btn = tk.Button(title_bar, text="✕", command=on_no,
                          bg=C["bg_header"], fg=C["text_dim"], font=FONT_UI,
                          activebackground=C["bg_header"], activeforeground=C["danger"],
                          relief=tk.FLAT, cursor="hand2", padx=8, pady=0,
                          borderwidth=0, highlightthickness=0)
    close_btn.pack(side=tk.RIGHT)

    # 拖拽事件（只对 title_bar 生效）
    def start_move(event):
        dialog.x = event.x
        dialog.y = event.y

    def do_move(event):
        dx = event.x_root - dialog.x - dialog.winfo_x()
        dy = event.y_root - dialog.y - dialog.winfo_y()
        dialog.geometry(f"+{event.x_root - dialog.x}+{event.y_root - dialog.y}")

    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<B1-Motion>", do_move)
    close_btn.bind("<Button-1>", lambda e: "break")  # 防止拖拽触发

    dialog.grab_set()
    dialog.wait_window()
    return result.get()


# ── 行卡片组件 ──
class ScriptRow(tk.Frame):
    """单行脚本卡片"""

    def __init__(self, parent, name, script, app, **kw):
        super().__init__(parent, bg=C["bg_card"], height=40, **kw)
        self.name = name
        self.script = script
        self.app = app
        self._hover = False

        self.pack_propagate(False)
        self.configure(cursor="hand2")

        # 内边距容器
        inner = tk.Frame(self, bg=C["bg_card"], padx=16, pady=4)
        inner.pack(fill=tk.BOTH, expand=True)

        # 状态指示点
        self.status_dot = tk.Canvas(inner, width=10, height=10, bg=C["bg_card"],
                                    highlightthickness=0)
        self.status_dot.pack(side=tk.LEFT, padx=(0, 12))
        self.dot_id = self.status_dot.create_oval(2, 2, 8, 8, fill=C["idle"], outline="")

        # 脚本名称
        self.name_label = tk.Label(inner, text=name, bg=C["bg_card"], fg=C["text"],
                                   font=FONT_MONO, anchor=tk.W)
        self.name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 上次运行时间
        self.time_label = tk.Label(inner, text="从未运行", bg=C["bg_card"], fg=C["text_dim"],
                                   font=FONT_MONO_SM, anchor=tk.E, width=20)
        self.time_label.pack(side=tk.RIGHT, padx=(8, 12))

        # 状态文字
        self.status_label = tk.Label(inner, text="○ 空闲", bg=C["bg_card"], fg=C["idle"],
                                     font=FONT_STATUS, anchor=tk.E, width=8)
        self.status_label.pack(side=tk.RIGHT, padx=(0, 12))

        # 操作按钮（悬停时显示）
        self.btn_start = tk.Button(inner, text="▶ 启动", command=self._on_start,
                                   bg=C["accent_dim"], fg=C["accent"], font=FONT_MONO_SM,
                                   activebackground="#002233", activeforeground=C["accent"],
                                   relief=tk.FLAT, cursor="hand2", padx=10, pady=1,
                                   borderwidth=0, highlightthickness=0)
        self.btn_stop = tk.Button(inner, text="■ 终止", command=self._on_stop,
                                  bg="#1a0a0a", fg=C["danger"], font=FONT_MONO_SM,
                                  activebackground="#330000", activeforeground=C["danger"],
                                  relief=tk.FLAT, cursor="hand2", padx=10, pady=1,
                                  borderwidth=0, highlightthickness=0)

        # 绑定事件（含按钮，防止鼠标移到按钮上时 Leave 导致按钮消失）
        for w in (self, inner, self.name_label, self.time_label, self.status_label,
                  self.status_dot, self.btn_start, self.btn_stop):
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)
            w.bind("<Double-Button-1>", lambda e: self._on_start())
            w.bind("<Button-1>", lambda e: self._on_click())

        self.update_display()

    def _on_enter(self, event):
        self._hover = True
        self.configure(bg=C["bg_card_hover"])
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=C["bg_card_hover"])
                for c in child.winfo_children():
                    try:
                        if not isinstance(c, tk.Button):
                            c.configure(bg=C["bg_card_hover"])
                    except:
                        pass
        self._update_buttons()

    def _on_leave(self, event):
        self._hover = False
        self.configure(bg=C["bg_card"])
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=C["bg_card"])
                for c in child.winfo_children():
                    try:
                        if not isinstance(c, tk.Button):
                            c.configure(bg=C["bg_card"])
                    except:
                        pass
        self._update_buttons()

    def _on_click(self, event=None):
        self.app.select_row(self)

    def _update_buttons(self):
        if self._hover:
            self.btn_start.pack(side=tk.RIGHT, padx=(4, 0))
            running = is_running(self.name)
            if running:
                self.btn_stop.pack(side=tk.RIGHT, padx=(4, 0))
            else:
                self.btn_stop.pack_forget()
        else:
            self.btn_start.pack_forget()
            self.btn_stop.pack_forget()

    def _on_start(self):
        if is_running(self.name):
            if not ask_confirm("防呆确认",
                               f"【{self.name}】正在运行中！\n\n确定要重新启动吗？"):
                return
            kill_script(self.name)
        launch_script(self.name, self.script)
        self.app.refresh_all()

    def _on_stop(self):
        if is_running(self.name):
            if ask_confirm("确认终止", f"确认终止 【{self.name}】？"):
                kill_script(self.name)
                self.app.refresh_all()

    def update_display(self):
        """刷新显示"""
        running = is_running(self.name)
        if running:
            color = C["running"]
            self.status_dot.itemconfig(self.dot_id, fill=color)
            self.status_label.configure(text="● 运行中", fg=color)
        else:
            color = C["idle"]
            self.status_dot.itemconfig(self.dot_id, fill=color)
            self.status_label.configure(text="○ 空闲", fg=color)
        last = history.get(self.name, "从未运行")
        if last != "从未运行":
            try:
                last_date = last[:10]  # "YYYY-MM-DD"
                today = datetime.now().strftime("%Y-%m-%d")
                if last_date != today:
                    last = last + "  (今天未执行)"
                    self.time_label.configure(text=last, fg=C["warning"])
                    self._update_buttons()
                    return
            except (ValueError, IndexError):
                pass
        self.time_label.configure(text=last, fg=C["text_dim"])
        self._update_buttons()

    def set_selected(self, selected):
        if selected:
            self.configure(bg=C["bg_card_hover"])
            for child in self.winfo_children():
                if isinstance(child, tk.Frame):
                    child.configure(bg=C["bg_card_hover"])
                    for c in child.winfo_children():
                        try:
                            if not isinstance(c, tk.Button):
                                c.configure(bg=C["bg_card_hover"])
                        except:
                            pass
        else:
            self.configure(bg=C["bg_card"])
            for child in self.winfo_children():
                if isinstance(child, tk.Frame):
                    child.configure(bg=C["bg_card"])
                    for c in child.winfo_children():
                        try:
                            if not isinstance(c, tk.Button):
                                c.configure(bg=C["bg_card"])
                        except:
                            pass


# ── 主窗口 ──
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("STELLAR SCRIPT HUB")
        self.root.configure(bg=C["bg_dark"])
        w, h = 620, 540
        x = root.winfo_screenwidth() // 2 - w // 2
        y = root.winfo_screenheight() // 2 - h // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.minsize(520, 400)

        self.rows = {}       # name -> ScriptRow
        self.selected = None

        self._build_header()
        self._build_body()
        self._build_footer()
        self._update_clock()
        self._schedule_poll()

    def _build_header(self):
        """顶部标题栏"""
        header = tk.Frame(self.root, bg=C["bg_header"], height=44, padx=16)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Logo
        logo = tk.Frame(header, bg=C["accent_dim"], padx=2, pady=2, highlightbackground=C["border_glow"],
                        highlightthickness=1)
        logo.pack(side=tk.LEFT, pady=8)
        tk.Label(logo, text="◈", bg=C["accent_dim"], fg=C["accent"],
                 font=("Consolas", 14, "bold")).pack(padx=6, pady=1)

        tk.Label(header, text="  STELLAR SCRIPT HUB", bg=C["bg_header"], fg=C["text"],
                 font=FONT_TITLE, anchor=tk.W).pack(side=tk.LEFT)

        # 时钟
        self.clock_label = tk.Label(header, text="", bg=C["bg_header"], fg=C["accent"],
                                    font=FONT_MONO_SM, anchor=tk.E)
        self.clock_label.pack(side=tk.RIGHT, padx=12)

        dot = tk.Canvas(header, width=8, height=8, bg=C["bg_header"], highlightthickness=0)
        dot.pack(side=tk.RIGHT, padx=(8, 0))
        dot.create_oval(1, 1, 7, 7, fill=C["success"], outline="")

    def _build_body(self):
        """可滚动脚本列表"""
        # 滚动区域容器
        list_bg = tk.Frame(self.root, bg=C["bg_dark"], padx=12, pady=6)
        list_bg.pack(fill=tk.BOTH, expand=True)

        # Canvas + Scrollbar 模拟滚动
        self.canvas = tk.Canvas(list_bg, bg=C["bg_dark"], highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(list_bg, orient=tk.VERTICAL, command=self.canvas.yview,
                                 bg=C["bg_card"], troughcolor=C["bg_dark"],
                                 activebackground=C["border_glow_dim"],
                                 highlightthickness=0, bd=0, width=6)
        self.scroll_frame = tk.Frame(self.canvas, bg=C["bg_dark"])

        self.scroll_frame.bind("<Configure>",
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", tags="inner")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 鼠标滚轮
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig("inner", width=e.width))

        self._populate_rows()

    def _get_sorted_items(self):
        """按最后运行时间倒序排列，运行中的排最前"""
        today = datetime.now().strftime("%Y-%m-%d")

        def sort_key(item):
            name = item[0]
            if is_running(name):
                return -2000000000  # 运行中排最前
            ts = history.get(name, "")
            if ts:
                try:
                    return -int(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").timestamp())
                except ValueError:
                    return 0
            return 0

        return sorted(gui_list, key=sort_key)

    def _populate_rows(self):
        for name, script in self._get_sorted_items():
            row = ScriptRow(self.scroll_frame, name, script, self)
            row.pack(fill=tk.X, pady=2)
            self.rows[name] = row

    def _reorder_rows(self):
        """按时间倒序重新排列行"""
        ordered = self._get_sorted_items()
        for name, _ in ordered:
            if name in self.rows:
                self.rows[name].pack(fill=tk.X, pady=2)

    def _build_footer(self):
        """底部按钮栏"""
        footer = tk.Frame(self.root, bg=C["bg_header"], height=48, padx=16)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        def make_btn(parent, text, command, accent=False, danger=False):
            if accent:
                bg, fg = C["accent_dim"], C["accent"]
            elif danger:
                bg, fg = "#1a0a0a", C["danger"]
            else:
                bg, fg = C["bg_card"], C["text_dim"]
            btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                            font=FONT_MONO_SM, activebackground=C["bg_card_hover"],
                            activeforeground=C["text"], relief=tk.FLAT, cursor="hand2",
                            padx=16, pady=4, borderwidth=0, highlightthickness=0)
            btn.bind("<Enter>", lambda e: btn.configure(bg=C["bg_card_hover"], fg=C["accent"] if accent else C["text"]))
            btn.bind("<Leave>", lambda e: btn.configure(bg=bg, fg=fg))
            return btn

        self.btn_start = make_btn(footer, "▶  启动", self._start_selected, accent=True)
        self.btn_start.pack(side=tk.LEFT, padx=(0, 8), pady=6)

        self.btn_stop = make_btn(footer, "■  终止", self._stop_selected, danger=True)
        self.btn_stop.pack(side=tk.LEFT, padx=8, pady=6)

        make_btn(footer, "↻  刷新", self.refresh_all).pack(side=tk.LEFT, padx=8, pady=6)

        make_btn(footer, "✕  退出", self.root.destroy).pack(side=tk.RIGHT, padx=(8, 0), pady=6)

        # 快捷键提示
        tk.Label(footer, text="双击=启动  ·  Enter=启动  ·  Delete=终止",
                 bg=C["bg_header"], fg=C["text_dim"], font=("Consolas", 8)).pack(side=tk.RIGHT, padx=16, pady=6)

    def _update_clock(self):
        self.clock_label.configure(text=datetime.now().strftime("%H:%M:%S  UTC+8"))
        self.root.after(1000, self._update_clock)

    # ── 选中 ──
    def select_row(self, row):
        if self.selected and self.selected in self.rows.values():
            self.selected.set_selected(False)
        self.selected = row
        row.set_selected(True)
        self._update_button_state()

    def _update_button_state(self):
        if self.selected is None:
            return
        name = self.selected.name
        running = is_running(name)
        # 底部按钮不做 disable，靠实际逻辑判断（tk.Button state 不好看）

    # ── 操作 ──
    def _start_selected(self):
        if self.selected:
            self.selected._on_start()
        elif self.rows:
            # 无选中时提示
            pass

    def _stop_selected(self):
        if self.selected:
            self.selected._on_stop()

    def refresh_all(self):
        cleanup_dead()
        for name, row in self.rows.items():
            row.update_display()
        self._reorder_rows()

    def _schedule_poll(self):
        self.refresh_all()
        self.root.after(POLL_INTERVAL_MS, self._schedule_poll)


# ── 入口 ──
if __name__ == "__main__":
    history = load_history()
    root = tk.Tk()
    app = App(root)
    # 键盘快捷键
    root.bind("<Return>", lambda e: app._start_selected())
    root.bind("<Delete>", lambda e: app._stop_selected())
    root.mainloop()
