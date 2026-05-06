import json
import os
import subprocess
import sys
import threading
import tkinter as tk
from datetime import datetime
from tkinter import font as tkfont
from tkinter import ttk

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

running_processes = {}          # name -> subprocess.Popen
log_tabs = {}                   # name -> {"text": Text, "frame": Frame, "done": bool, "generation": int,
                                #            "tmpfile": str (temp file path for stdout capture)}
log_generation = {}             # name -> int (prevents stale reader from removing new tab)
log_read_pos = {}               # name -> int (bytes already read from tmpfile)
CREATE_NEW_PROCESS_GROUP = 0x00000200
POLL_INTERVAL_MS = 2000

# ── 全局引用，供后台读线程回调 ──
_app = None

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
FONT_LOG = ("Consolas", 9)


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

    # 递增代次，防止旧线程错误销毁新页签
    log_generation[name] = log_generation.get(name, 0) + 1
    gen = log_generation[name]

    # 使用临时文件捕获 stdout，避免 Windows PIPE 在 easygui 阻塞时的缓冲问题
    import tempfile
    fd, tmpfile_path = tempfile.mkstemp(suffix='.log', prefix='gui_')
    os.close(fd)  # 关闭 os 级句柄，后面用 open() 以文本模式重开

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    # 子进程 stdout/stderr 全部写入临时文件
    log_fd = open(tmpfile_path, 'w', encoding='utf-8')
    proc = subprocess.Popen(
        [sys.executable, "-u", script],
        stdout=log_fd,
        stderr=subprocess.STDOUT,
        env=env,
        creationflags=CREATE_NEW_PROCESS_GROUP,
    )
    running_processes[name] = proc

    # 记录临时文件路径
    if name not in log_tabs:
        log_tabs[name] = {}
    log_tabs[name]["tmpfile"] = tmpfile_path
    log_tabs[name]["done"] = False
    log_tabs[name]["generation"] = gen
    log_read_pos[name] = 0  # 重置读取位置

    # 立即关闭主进程持有的文件句柄（子进程已继承）
    log_fd.close()


def _read_tmpfile(name):
    """从临时文件读取新增内容，投递到日志窗口"""
    if name not in log_tabs or "tmpfile" not in log_tabs[name]:
        return
    tmpfile_path = log_tabs[name]["tmpfile"]
    try:
        pos = log_read_pos.get(name, 0)
        with open(tmpfile_path, 'r', encoding='utf-8') as f:
            f.seek(pos)
            new_data = f.read()
            if new_data:
                log_read_pos[name] = f.tell()
                # 逐行投递
                for line in new_data.splitlines(True):
                    if _app:
                        _app.append_log(name, line)
    except FileNotFoundError:
        pass
    except Exception:
        pass


def kill_script(name):
    proc = running_processes.get(name)
    if proc and proc.poll() is None:
        try:
            proc.kill()
        except Exception:
            pass
        try:
            # 强制 terminate（Windows TerminateProcess），easygui/tkinter 前端也管用
            proc.terminate()
        except Exception:
            pass
        # 不调用 wait()，让 poll 循环处理回收
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

    # 拖拽事件
    def start_move(event):
        dialog.x = event.x
        dialog.y = event.y

    def do_move(event):
        dialog.geometry(f"+{event.x_root - dialog.x}+{event.y_root - dialog.y}")

    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<B1-Motion>", do_move)
    close_btn.bind("<Button-1>", lambda e: "break")

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
        self.app._ensure_log_tab(self.name)
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
                last_date = last[:10]
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
        global _app
        _app = self

        self.root = root
        self.root.title("STELLAR SCRIPT HUB")
        self.root.configure(bg=C["bg_dark"])
        w, h = 960, 540
        x = root.winfo_screenwidth() // 2 - w // 2
        y = root.winfo_screenheight() // 2 - h // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.minsize(720, 400)

        self.rows = {}          # name -> ScriptRow
        self.selected = None

        self._setup_ttk_style()
        self._build_header()
        self._build_body()
        self._build_footer()
        self._update_clock()
        self._schedule_poll()

    def _setup_ttk_style(self):
        """配置 Notebook 暗色主题"""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TNotebook",
                        background=C["bg_dark"],
                        borderwidth=0,
                        tabmargins=[0, 0, 0, 0])
        style.configure("TNotebook.Tab",
                        background=C["bg_card"],
                        foreground=C["text_dim"],
                        padding=[14, 5],
                        font=FONT_MONO_SM,
                        borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", C["accent_dim"])],
                  foreground=[("selected", C["accent"])],
                  expand=[("selected", [2, 2, 2, 0])])
        style.configure("TFrame", background=C["bg_dark"])

    def _build_header(self):
        """顶部标题栏"""
        header = tk.Frame(self.root, bg=C["bg_header"], height=44, padx=16)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Logo
        logo = tk.Frame(header, bg=C["accent_dim"], padx=2, pady=2,
                        highlightbackground=C["border_glow"], highlightthickness=1)
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
        """左右分栏布局：左侧脚本列表 + 右侧日志百叶窗"""
        # ── PanedWindow 分栏 ──
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL,
                                     bg=C["border"], sashwidth=3,
                                     sashrelief=tk.FLAT, sashpad=1)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # ── 左侧：脚本列表 ──
        left_frame = tk.Frame(self.paned, bg=C["bg_dark"])
        self.paned.add(left_frame, width=480, minsize=300)
        self._build_left_panel(left_frame)

        # ── 右侧：日志百叶窗 ──
        right_frame = tk.Frame(self.paned, bg=C["bg_dark"])
        self.paned.add(right_frame, width=480, minsize=200)
        self._build_right_panel(right_frame)

    def _build_left_panel(self, parent):
        """左侧可滚动脚本列表"""
        list_bg = tk.Frame(parent, bg=C["bg_dark"], padx=12, pady=6)
        list_bg.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(list_bg, bg=C["bg_dark"], highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(list_bg, orient=tk.VERTICAL, command=self.canvas.yview,
                                 bg=C["bg_card"], troughcolor=C["bg_dark"],
                                 activebackground=C["border_glow_dim"],
                                 highlightthickness=0, bd=0, width=6)
        self.scroll_frame = tk.Frame(self.canvas, bg=C["bg_dark"])

        self.scroll_frame.bind("<Configure>",
                               lambda e: self.canvas.configure(
                                   scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame,
                                  anchor="nw", tags="inner")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig("inner", width=e.width))

        self._populate_rows()

    def _build_right_panel(self, parent):
        """右侧日志百叶窗（ttk.Notebook）"""
        # 容器
        right_container = tk.Frame(parent, bg=C["bg_dark"])
        right_container.pack(fill=tk.BOTH, expand=True)

        # 标题
        self.log_header = tk.Frame(right_container, bg=C["bg_dark"], height=26)
        self.log_header.pack(fill=tk.X)
        self.log_header.pack_propagate(False)
        tk.Label(self.log_header, text="◆  日志视图", bg=C["bg_dark"],
                 fg=C["text_dim"], font=("Consolas", 9, "bold"),
                 anchor=tk.W).pack(side=tk.LEFT)

        # 运行计数标签
        self.log_count_label = tk.Label(self.log_header, text="",
                                        bg=C["bg_dark"], fg=C["accent"],
                                        font=FONT_MONO_SM, anchor=tk.E)
        self.log_count_label.pack(side=tk.RIGHT)

        # Notebook
        self.notebook = ttk.Notebook(right_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        # 占位标签（无日志时显示）
        self.placeholder_frame = tk.Frame(right_container, bg=C["bg_dark"])
        self._show_log_placeholder()

    def _show_log_placeholder(self):
        """显示"暂无运行中脚本"占位"""
        self.placeholder_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER,
                                      x=0, y=20)
        for w in self.placeholder_frame.winfo_children():
            w.destroy()
        tk.Label(self.placeholder_frame, text="◈", bg=C["bg_dark"],
                 fg=C["border"], font=("Consolas", 28)).pack()
        tk.Label(self.placeholder_frame, text="暂无运行中脚本",
                 bg=C["bg_dark"], fg=C["text_dim"],
                 font=("Microsoft YaHei", 10)).pack(pady=(4, 0))
        tk.Label(self.placeholder_frame, text="启动左侧脚本后将在此显示实时日志",
                 bg=C["bg_dark"], fg=C["border"],
                 font=("Microsoft YaHei", 8)).pack()

    def _hide_log_placeholder(self):
        self.placeholder_frame.place_forget()

    # ── 日志页签管理 ──
    def _ensure_log_tab(self, name):
        """为脚本创建（或复用）日志页签"""
        if name in log_tabs and "frame" in log_tabs[name]:
            # 复用已有页签：清空文本，重置 done 标记
            info = log_tabs[name]
            info["done"] = False
            info["generation"] = log_generation.get(name, 0)
            text_w = info["text"]
            text_w.configure(state=tk.NORMAL)
            text_w.delete("1.0", tk.END)
            text_w.insert(tk.END, f"◆ 脚本 [{name}] 启动中...\n", "accent")
            text_w.see(tk.END)
            text_w.configure(state=tk.DISABLED)
            # 切换到该页签
            self.notebook.select(info["frame"])
            self._hide_log_placeholder()
            self._update_log_count()
            return

        # 创建新页签
        tab_frame = ttk.Frame(self.notebook)

        # 工具栏
        tab_toolbar = tk.Frame(tab_frame, bg=C["bg_header"], height=28)
        tab_toolbar.pack(fill=tk.X)
        tab_toolbar.pack_propagate(False)
        tk.Label(tab_toolbar, text=f"  {name}", bg=C["bg_header"],
                 fg=C["accent"], font=FONT_MONO_SM, anchor=tk.W).pack(side=tk.LEFT)

        # 关闭按钮
        def _close_tab():
            self._remove_log_tab(name)

        close_btn = tk.Button(tab_toolbar, text="✕", command=_close_tab,
                              bg=C["bg_header"], fg=C["text_dim"],
                              font=FONT_UI, relief=tk.FLAT, cursor="hand2",
                              padx=8, pady=0, borderwidth=0, highlightthickness=0,
                              activebackground=C["bg_header"],
                              activeforeground=C["danger"])
        close_btn.pack(side=tk.RIGHT)

        # 日志文本域
        text_frame = tk.Frame(tab_frame, bg=C["bg_input"])
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_w = tk.Text(text_frame, bg=C["bg_input"], fg=C["text"],
                         font=FONT_LOG, wrap=tk.WORD, state=tk.DISABLED,
                         insertbackground=C["accent"],
                         selectbackground=C["accent_dim"],
                         selectforeground=C["text"],
                         relief=tk.FLAT, borderwidth=0,
                         padx=10, pady=6,
                         yscrollcommand=None)
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL,
                                 command=text_w.yview,
                                 bg=C["bg_card"], troughcolor=C["bg_input"],
                                 activebackground=C["border_glow_dim"],
                                 highlightthickness=0, bd=0, width=6)
        text_w.configure(yscrollcommand=scrollbar.set)
        text_w.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 配置文本 tag 样式
        text_w.tag_configure("dim", foreground=C["text_dim"])
        text_w.tag_configure("accent", foreground=C["accent"])
        text_w.tag_configure("warn", foreground=C["warning"])
        text_w.tag_configure("error", foreground=C["danger"])
        text_w.tag_configure("exit", foreground=C["success"])

        # 写入启动提示
        text_w.configure(state=tk.NORMAL)
        text_w.insert(tk.END, f"◆ 脚本 [{name}] 启动中...\n", "accent")
        text_w.configure(state=tk.DISABLED)

        self.notebook.add(tab_frame, text=f"  {name}  ")
        self.notebook.select(tab_frame)

        # 记录
        if name not in log_tabs:
            log_tabs[name] = {}
        log_tabs[name].update({
            "frame": tab_frame,
            "text": text_w,
            "done": False,
            "generation": log_generation.get(name, 0),
        })

        self._hide_log_placeholder()
        self._update_log_count()

    def append_log(self, name, line):
        """供后台线程调用，将日志行投递到主线程"""
        self.root.after(0, lambda: self._append_log_main(name, line))

    def _append_log_main(self, name, line):
        """主线程中实际追加日志文本，全量输出所有日志等级"""
        if name not in log_tabs or "text" not in log_tabs[name]:
            return
        text_w = log_tabs[name]["text"]
        text_w.configure(state=tk.NORMAL)

        # 着色：debug(dim) / info(default) / warning(orange) / error(red)
        lower = line.lower()
        if any(kw in lower for kw in ("error", "exception", "traceback", "failed", "错误", "失败", "异常")):
            tag = "error"
        elif any(kw in lower for kw in ("warning", "warn", "警告")):
            tag = "warn"
        elif any(kw in lower for kw in ("debug", "调试")):
            tag = "dim"
        else:
            tag = None

        if tag:
            text_w.insert(tk.END, line, tag)
        else:
            text_w.insert(tk.END, line)

        text_w.see(tk.END)
        text_w.configure(state=tk.DISABLED)

    def _remove_log_tab(self, name):
        """销毁日志页签，同时清理临时文件"""
        if name not in log_tabs:
            return
        info = log_tabs.pop(name, None)
        if info:
            # 清理临时文件
            tmpfile_path = info.get("tmpfile")
            if tmpfile_path and os.path.exists(tmpfile_path):
                try:
                    os.unlink(tmpfile_path)
                except Exception:
                    pass
            if "frame" in info:
                try:
                    self.notebook.forget(info["frame"])
                    info["frame"].destroy()
                except Exception:
                    pass

        log_read_pos.pop(name, None)
        self._update_log_count()
        active_tabs = [n for n in log_tabs if "frame" in log_tabs[n]]
        if not active_tabs:
            self._show_log_placeholder()

    def _finalize_dead_tabs(self):
        """遍历 log_tabs，对进程已退出的页签写入结束标记"""
        for name in list(log_tabs.keys()):
            info = log_tabs[name]
            if info.get("done"):
                continue  # 已经标记过结束
            proc = running_processes.get(name)
            # 进程不在运行中（已被 cleanup_dead 清除，或从未启动成功）
            if proc is None:
                info["done"] = True
                if "text" in info:
                    try:
                        text_w = info["text"]
                        text_w.configure(state=tk.NORMAL)
                        text_w.insert(tk.END, "\n── 进程结束 ──\n", "exit")
                        text_w.see(tk.END)
                        text_w.configure(state=tk.DISABLED)
                    except Exception:
                        pass

    def _update_log_count(self):
        """更新右上角运行计数"""
        active = sum(1 for n in log_tabs if "frame" in log_tabs[n]
                     and not log_tabs[n].get("done", False))
        if active > 0:
            self.log_count_label.configure(
                text=f"运行中: {active}  ")
        else:
            self.log_count_label.configure(text="")

    def _get_sorted_items(self):
        """按最后运行时间倒序排列，运行中的排最前"""
        def sort_key(item):
            name = item[0]
            if is_running(name):
                return -2000000000
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
            btn.bind("<Enter>", lambda e, b=btn, a=accent:
                     b.configure(bg=C["bg_card_hover"],
                                 fg=C["accent"] if a else C["text"]))
            btn.bind("<Leave>", lambda e, b=btn, _bg=bg, _fg=fg:
                     b.configure(bg=_bg, fg=_fg))
            return btn

        self.btn_start = make_btn(footer, "▶  启动", self._start_selected, accent=True)
        self.btn_start.pack(side=tk.LEFT, padx=(0, 8), pady=6)

        self.btn_stop = make_btn(footer, "■  终止", self._stop_selected, danger=True)
        self.btn_stop.pack(side=tk.LEFT, padx=8, pady=6)

        make_btn(footer, "↻  刷新", self.refresh_all).pack(side=tk.LEFT, padx=8, pady=6)

        make_btn(footer, "✕  退出", self._on_exit).pack(side=tk.RIGHT,
                                                          padx=(8, 0), pady=6)

        tk.Label(footer, text="双击=启动  ·  Enter=启动  ·  Delete=终止",
                 bg=C["bg_header"], fg=C["text_dim"],
                 font=("Consolas", 8)).pack(side=tk.RIGHT, padx=16, pady=6)

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

    # ── 操作 ──
    def _start_selected(self):
        if self.selected:
            self.selected._on_start()

    def _stop_selected(self):
        if self.selected:
            self.selected._on_stop()

    def refresh_all(self):
        """刷新所有状态：读取日志 + 清理死进程 + 更新显示 + 重排"""
        # 先读取所有运行中进程的临时文件日志
        for name in list(running_processes.keys()):
            _read_tmpfile(name)

        cleanup_dead()

        # 标记已死进程的日志页签（写入结束标记）
        self._finalize_dead_tabs()

        # 清理已结束的日志页签（仅 done=True 且进程确实不存在的）
        for name in list(log_tabs.keys()):
            info = log_tabs[name]
            proc = running_processes.get(name)
            if info.get("done", False) and proc is None:
                self._remove_log_tab(name)

        for name, row in self.rows.items():
            row.update_display()
        self._reorder_rows()
        self._update_log_count()

    def _schedule_poll(self):
        self.refresh_all()
        self.root.after(POLL_INTERVAL_MS, self._schedule_poll)

    def _kill_all_children(self):
        """强制杀死所有子进程"""
        for name, proc in list(running_processes.items()):
            try:
                proc.kill()
            except Exception:
                pass
            try:
                proc.terminate()
            except Exception:
                pass
        # 清理临时文件
        for name in list(log_tabs.keys()):
            self._remove_log_tab(name)

    def _on_exit(self):
        """退出前杀死所有子进程"""
        self._kill_all_children()
        self.root.destroy()


# ── 入口 ──
if __name__ == "__main__":
    history = load_history()
    root = tk.Tk()
    app = App(root)
    root.bind("<Return>", lambda e: app._start_selected())
    root.bind("<Delete>", lambda e: app._stop_selected())
    root.protocol("WM_DELETE_WINDOW", app._on_exit)  # 点 X 也杀进程
    root.mainloop()
