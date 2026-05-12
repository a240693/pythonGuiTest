import time
import cv2
import ctypes
import ctypes.wintypes
import subprocess
import numpy as np
import win32gui
import win32ui
import win32con
import win32api
import win32process
from . import dao
from . import changeVar as cv

user32 = ctypes.windll.user32

# declare Per-Monitor DPI V2 awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        user32.SetProcessDPIAware()
    except Exception:
        pass

path = cv.path


class Photo:
    def __init__(self, window_title=None, debug=False, click_offset_x=0,
                 click_offset_y=0, click_method="postmessage",
                 adb_device=None):
        """
        bg Photo: bg screenshot + template match + background click.

        :param window_title: fuzzy match window by title/class/process
        :param debug: if True, save debug screenshots with click markers
        :param click_offset_x/y: fine-tune offset in screenshot pixels
        :param click_method: "postmessage" | "sendmessage" | "sendinput" | "adb"
               - postmessage: PostMessage (async, may not work with DX games)
               - sendmessage: SendMessage (sync, more likely handled)
               - sendinput: SendInput via system queue (briefly focuses window)
               - adb: adb shell input tap (for Android emulators, bypasses
                 all Windows coordinate issues, completely background-safe)
        :param adb_device: adb device serial (e.g. "emulator-5554").
               If None, auto-detect from 'adb devices'.
        """
        self.name = "default"
        self.x = 0
        self.y = 0
        self.hwnd = None
        self.process_name = ""
        self.debug = debug
        self.click_offset_x = click_offset_x
        self.click_offset_y = click_offset_y
        self.click_method = click_method
        self.adb_device = adb_device
        self._adb_device_cached = None  # lazily resolved
        self._dpi_scale = 1.0
        self._capture_w = 0
        self._capture_h = 0
        global path
        path = cv.get_value("path")
        if window_title is None:
            try:
                window_title = cv.get_value("window_title")
            except Exception:
                window_title = "SDgundam"
        self.window_title = window_title
        self._refresh_hwnd()
        if self.debug:
            self._inspect_window_hierarchy()

    # ---------- window management ----------

    @staticmethod
    def _get_process_name(hwnd):
        """get process name from window handle"""
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            kernel32 = ctypes.windll.kernel32
            PROCESS_QUERY_INFORMATION = 0x0400
            PROCESS_VM_READ = 0x0010
            h_process = kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
            if h_process:
                exe_name = ctypes.create_unicode_buffer(260)
                size = ctypes.c_uint32(260)
                if kernel32.QueryFullProcessImageNameW(
                        h_process, 0, ctypes.byref(exe_name),
                        ctypes.byref(size)):
                    full_path = exe_name.value
                    kernel32.CloseHandle(h_process)
                    return full_path.split("\\")[-1].lower()
                kernel32.CloseHandle(h_process)
        except Exception:
            pass
        return ""

    @staticmethod
    def list_windows():
        """list all visible windows to help find window_title"""
        windows = []

        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                proc_name = Photo._get_process_name(hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                w = rect[2] - rect[0]
                h = rect[3] - rect[1]
                if title.strip():
                    extra.append((hwnd, title, class_name, proc_name, w, h))
            return True

        win32gui.EnumWindows(callback, windows)
        windows.sort(key=lambda x: x[1])

        print("=" * 90)
        print("{:<45} {:<25} {:<8} {:<8}".format(
            "title", "process/class", "w", "h"))
        print("=" * 90)
        for hwnd, title, class_name, proc_name, w, h in windows:
            print("{:<45} {:<25} {:<8} {:<8}".format(
                title[:43], "{}/{}".format(proc_name[:12], class_name[:10]),
                w, h))
        print("=" * 90)
        print("total {} visible windows".format(len(windows)))
        return windows

    def _refresh_hwnd(self):
        """fuzzy match window: title -> class -> process"""
        hwnd_list = []

        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                keyword = self.window_title
                if keyword in title:
                    extra.append((hwnd, 1))
                elif keyword in class_name:
                    extra.append((hwnd, 2))
                elif keyword in Photo._get_process_name(hwnd):
                    extra.append((hwnd, 3))
            return True

        win32gui.EnumWindows(callback, hwnd_list)
        if hwnd_list:
            hwnd_list.sort(key=lambda x: x[1])
            self.hwnd = hwnd_list[0][0]
            self.process_name = Photo._get_process_name(self.hwnd)
            print("found: {} proc: {} hwnd: {}".format(
                win32gui.GetWindowText(self.hwnd),
                self.process_name, self.hwnd))
        else:
            self.hwnd = None
            self.process_name = ""
            print("warn: no visible window matching: {}".format(
                self.window_title))
            print("hint: use Photo.list_windows()")

    def _inspect_window_hierarchy(self):
        """debug: enumerate child windows under hwnd to find real input target"""
        if not self.hwnd:
            return
        try:
            children = []

            def child_callback(hwnd, extra):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    cls = win32gui.GetClassName(hwnd)
                    rect = win32gui.GetWindowRect(hwnd)
                    cr = win32gui.GetClientRect(hwnd)
                    w, h_ = rect[2] - rect[0], rect[3] - rect[1]
                    cw, ch = cr[2] - cr[0], cr[3] - cr[1]
                    if w > 0 and cw > 0:
                        extra.append((hwnd, title, cls, w, h_, cw, ch))
                return True

            win32gui.EnumChildWindows(self.hwnd, child_callback, children)
            if children:
                print("--- window hierarchy for hwnd={} ---".format(self.hwnd))
                print("  parent: '{}' cls={}".format(
                    win32gui.GetWindowText(self.hwnd),
                    win32gui.GetClassName(self.hwnd)))
                for h, t, c, w, h_, cw, ch in children:
                    print("  child: hwnd={} '{}' cls={} win={}x{}"
                          " client={}x{}".format(
                              h, t, c, w, h_, cw, ch))
                print("--- {} child windows found ---".format(len(children)))
            else:
                print("--- no visible children under hwnd={} ---".format(
                    self.hwnd))
        except Exception as e:
            print("inspect hierarchy failed: {}".format(e))

    def _get_window_dpi_scale(self):
        """
        Detect DPI scale of the target window.
        Returns scale = physical_pixels / logical_coords.
        > 1.0 means high-DPI: PostMessage needs *smaller* logical coords.
        Also compares capture dimensions with client rect for sanity check.
        """
        if not self.hwnd:
            return 1.0

        dpi = 96
        try:
            # Windows 10 1607+: per-window DPI
            gdfw = user32.GetDpiForWindow
            dpi = gdfw(self.hwnd)
        except Exception:
            try:
                # fallback: system DPI via screen DC
                hdc = user32.GetDC(0)
                dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
                user32.ReleaseDC(0, hdc)
            except Exception:
                pass

        scale = dpi / 96.0

        # sanity: if we have capture dimensions, compare with client rect
        if self._capture_w > 0:
            try:
                cr = win32gui.GetClientRect(self.hwnd)
                logical_w = cr[2] - cr[0]
                logical_h = cr[3] - cr[1]
                # Per-Monitor V2 鈫?GetClientRect returns physical px
                # but if target is not DPI-aware, Windows may return logical px
                ratio_w = self._capture_w / max(logical_w, 1)
                ratio_h = self._capture_h / max(logical_h, 1)
                if abs(ratio_w - scale) > 0.05 or abs(ratio_h - scale) > 0.05:
                    # mismatch 鈥?trust the image vs GetClientRect ratio
                    scale = max(ratio_w, ratio_h)
            except Exception:
                pass

        self._dpi_scale = round(scale, 4)
        print("dpi: target={} scale={} capture={}x{}".format(
            dpi, self._dpi_scale, self._capture_w, self._capture_h))
        return self._dpi_scale

    def _is_window_ok(self):
        """check if hwnd is valid and not minimized"""
        if self.hwnd is None:
            return False
        try:
            if not win32gui.IsWindow(self.hwnd):
                return False
            if win32gui.IsIconic(self.hwnd):
                return False
            return True
        except Exception:
            return False

    def _ensure_hwnd(self):
        """ensure valid hwnd, refresh if invalid"""
        if not self._is_window_ok():
            self._refresh_hwnd()
        return self.hwnd is not None

    # ---------- bg screenshot ----------

    def _capture_window(self):
        """
        bg capture client area: PrintWindow first, fallback BitBlt.
        flag=3: PW_RENDERFULLCONTENT(2)|PW_CLIENTONLY(1) - client area only, no title bar.
        Stores capture dimensions in self._capture_w / _capture_h for DPI calc.
        """
        if not self._ensure_hwnd():
            print("error: cannot get hwnd")
            return None

        try:
            client_rect = win32gui.GetClientRect(self.hwnd)
            width = client_rect[2] - client_rect[0]
            height = client_rect[3] - client_rect[1]

            if width <= 0 or height <= 0:
                print("invalid client size: {}x{}".format(width, height))
                return None

            hwnd_dc = win32gui.GetDC(self.hwnd)
            mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()

            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
            save_dc.SelectObject(bitmap)

            # flag=2: PW_RENDERFULLCONTENT - DirectX
            result = user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)

            if result == 1:
                bmp_info = bitmap.GetInfo()
                bmp_str = bitmap.GetBitmapBits(True)
                img = np.frombuffer(bmp_str, dtype=np.uint8).reshape(
                    bmp_info['bmHeight'], bmp_info['bmWidth'], 4)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                print("PrintWindow failed, fallback BitBlt")
                save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0),
                               win32con.SRCCOPY)
                bmp_info = bitmap.GetInfo()
                bmp_str = bitmap.GetBitmapBits(True)
                img = np.frombuffer(bmp_str, dtype=np.uint8).reshape(
                    bmp_info['bmHeight'], bmp_info['bmWidth'], 4)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwnd_dc)

            # store for DPI scale calculation
            self._capture_w = img.shape[1]
            self._capture_h = img.shape[0]

            return img

        except Exception as e:
            print("bg screenshot failed: {}".format(e))
            return None

    # ---------- template match ----------

    def _locate_image(self, template, screenshot, confidence=0.7,
                      grayscale=False):
        """match template in screenshot, return (x,y,w,h) or None"""
        if screenshot is None or template is None:
            return None

        try:
            if grayscale:
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            sh, sw = screenshot.shape[:2]
            th, tw = template.shape[:2]
            if th > sh or tw > sw:
                print("template({}x{}) > screenshot({}x{})".format(tw, th, sw, sh))
                return None

            result = cv2.matchTemplate(screenshot, template,
                                       cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= confidence:
                x, y = max_loc
                return (x, y, tw, th)
            else:
                return None
        except Exception as e:
            print("tm exception: {}".format(e))
            return None

    # ---------- bg click ----------

    def _get_screen_coords(self, x, y):
        """compute screen-space and logical coords from template match center"""
        scale = self._get_window_dpi_scale()
        screen_x = x + self.click_offset_x
        screen_y = y + self.click_offset_y
        logical_x = int(screen_x / scale) if scale != 0 else screen_x
        logical_y = int(screen_y / scale) if scale != 0 else screen_y
        return screen_x, screen_y, logical_x, logical_y, scale

    def _bg_click_postmessage(self, logical_x, logical_y):
        """PostMessage - async, low-level. Many DX games ignore this."""
        lparam = win32api.MAKELONG(logical_x, logical_y)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON, lparam)
        time.sleep(0.02)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lparam)

    def _find_click_target(self):
        """Find the deepest child window that likely receives input.
        Many games render to a child window (e.g. SDL/DirectX surface).
        Sending messages to the parent may be ignored.
        Returns the best child hwnd, or None if no suitable child found.
        """
        if not self.hwnd:
            return None
        try:
            children = []
            cr_target = win32gui.GetClientRect(self.hwnd)
            target_cw = cr_target[2] - cr_target[0]
            target_ch = cr_target[3] - cr_target[1]

            def enum_child(hwnd, extra):
                if win32gui.IsWindowVisible(hwnd):
                    cr = win32gui.GetClientRect(hwnd)
                    cw, ch = cr[2] - cr[0], cr[3] - cr[1]
                    if cw > 0 and ch > 0:
                        extra.append((hwnd, cw, ch))
                return True

            win32gui.EnumChildWindows(self.hwnd, enum_child, children)

            if not children:
                return None

            # prefer child with same client size as parent (render surface)
            for hwnd, cw, ch in children:
                if cw == target_cw and ch == target_ch:
                    if self.debug:
                        print("sendmessage: found render child hwnd=0x{:X} {}x{}".format(
                            hwnd, cw, ch))
                    return hwnd

            # fallback: largest child
            children.sort(key=lambda x: x[1] * x[2], reverse=True)
            best = children[0]
            if self.debug:
                print("sendmessage: using largest child hwnd=0x{:X} {}x{}".format(
                    best[0], best[1], best[2]))
            return best[0]
        except Exception as e:
            if self.debug:
                print("sendmessage: find target failed: {}".format(e))
            return None

    def _bg_click_sendmessage(self, logical_x, logical_y):
        """SendMessage - enhanced reliability for DX/OpenGL games.

        1. Resolve child window (games often render to a child hwnd)
        2. Send WM_MOUSEMOVE first to position cursor
        3. Send WM_LBUTTONDOWN/UP with proper wParam (0 for UP)
        4. Retry once if no response detected
        """
        # resolve target window: prefer deepest child with matching client size
        target_hwnd = self._find_click_target()
        if target_hwnd is None:
            target_hwnd = self.hwnd

        lparam = win32api.MAKELONG(logical_x, logical_y)
        if self.debug:
            print("sendmessage: target=0x{:X} msg=(WinProc)".format(target_hwnd))

        # helper to send a click cycle
        def _send_click_cycle(hw):
            win32api.SendMessage(hw, win32con.WM_MOUSEMOVE, 0, lparam)
            time.sleep(0.01)
            win32api.SendMessage(hw, win32con.WM_LBUTTONDOWN,
                                 win32con.MK_LBUTTON, lparam)
            time.sleep(0.05)
            win32api.SendMessage(hw, win32con.WM_LBUTTONUP, 0, lparam)

        # primary attempt
        _send_click_cycle(target_hwnd)
        time.sleep(0.05)

        # retry with parent hwnd if child may not handle input
        if target_hwnd != self.hwnd:
            if self.debug:
                print("sendmessage: retry on parent hwnd")
            _send_click_cycle(self.hwnd)

    def _bg_click_sendinput(self, screen_x, screen_y):
        """
        SendInput via win32api.mouse_event (system input queue).
        Most reliable for DirectX games but requires brief foreground focus.
        Calls _click_screen_coords which briefly activates window,
        converts client coords to screen coords, sends click, restores.
        """
        return self._click_screen_coords(screen_x, screen_y)

    def _adb_resolve_device(self):
        """lazily resolve adb device serial. returns None on failure."""
        if self._adb_device_cached is not None:
            return self._adb_device_cached if self._adb_device_cached else None

        if self.adb_device:
            # verify it exists
            try:
                result = subprocess.run(
                    ["adb", "-s", self.adb_device, "shell", "echo", "ok"],
                    capture_output=True, text=True, timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW)
                if "ok" in result.stdout:
                    self._adb_device_cached = self.adb_device
                    print("adb: device {} confirmed".format(self.adb_device))
                    return self.adb_device
            except Exception:
                pass
            print("adb: specified device '{}' not reachable".format(
                self.adb_device))
            self._adb_device_cached = ""
            return None

        # auto-detect
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True, text=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW)
            lines = result.stdout.strip().split("\n")[1:]
            for line in lines:
                if "device" in line and "\tdevice" in line:
                    serial = line.split("\t")[0]
                    self._adb_device_cached = serial
                    print("adb: auto-detected device {}".format(serial))
                    return serial
        except Exception as e:
            print("adb: auto-detect failed: {}".format(e))

        self._adb_device_cached = ""
        print("adb: no device found. Run 'adb devices' to check.")
        return None

    def _bg_click_adb(self, screen_x, screen_y):
        """
        adb shell input tap - directly taps Android coordinates.
        Screenshot pixel coords map 1:1 to Android display coords
        (assuming emulator renders at screenshot resolution).
        Completely bypasses all Windows coordinate systems.
        Fully background-safe: no window focus needed.
        """
        serial = self._adb_resolve_device()
        if not serial:
            print("adb: no device, click skipped")
            return False

        # screenshot coords 鈫?Android screen coords (1:1 for emulator)
        android_x = int(screen_x)
        android_y = int(screen_y)

        try:
            subprocess.run(
                ["adb", "-s", serial, "shell", "input", "tap",
                 str(android_x), str(android_y)],
                capture_output=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW)
            print("adb tap: ({}, {})".format(android_x, android_y))
            return True
        except Exception as e:
            print("adb tap failed: {}".format(e))
            return False

    def _click_screen_coords(self, client_x, client_y):
        """
        Convert client-area physical-pixel coords (from PrintWindow screenshot)
        to absolute screen coords for SetCursorPos / SendInput.

        Key fix: ClientToScreen expects LOGICAL client coordinates, but our
        screenshot is in PHYSICAL pixels. When the target window has DPI
        virtualization, we must divide by the DPI scale BEFORE calling
        ClientToScreen.
        """
        try:
            scale = self._dpi_scale if self._dpi_scale > 0 else 1.0
            # convert physical screenshot px 鈫?logical client coords
            logical_x = int(client_x / scale)
            logical_y = int(client_y / scale)
            # Use ClientToScreen API to convert logical client coords
            # to absolute screen coords. Correctly handles:
            # - window borders, title bar, menu bar
            # - DPI scaling (logical client -> physical screen)
            # - Win10 invisible shadow padding
            # Replaces error-prone manual frame calculation.
            screen_pt = win32gui.ClientToScreen(self.hwnd, (logical_x, logical_y))
            screen_x, screen_y = screen_pt


            if self.debug:
                rect = win32gui.GetWindowRect(self.hwnd)
                cr = win32gui.GetClientRect(self.hwnd)
                print("debug: winRect=({},{},{},{}) clientRect=({},{},{},{})".format(
                    rect[0], rect[1], rect[2], rect[3],
                    cr[0], cr[1], cr[2], cr[3]))
                print("debug: win=({}x{}) client=({}x{})".format(
                    rect[2]-rect[0], rect[3]-rect[1],
                    cr[2]-cr[0], cr[3]-cr[1]))
                print("debug: physical=({},{}) logical=({},{})"
                      " clienttoscreen=({},{}) scale={}".format(
                    client_x, client_y, logical_x, logical_y,
                    screen_x, screen_y, scale))

            fg_hwnd = user32.GetForegroundWindow()
            fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
            self_thread = ctypes.windll.kernel32.GetCurrentThreadId()
            user32.AttachThreadInput(self_thread, fg_thread, True)

            try:
                user32.SetForegroundWindow(self.hwnd)
                time.sleep(0.03)
            finally:
                user32.AttachThreadInput(self_thread, fg_thread, False)

            # SendInput via mouse_event (system queue)
            win32api.SetCursorPos((screen_x, screen_y))
            time.sleep(0.02)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,
                                 screen_x, screen_y, 0, 0)
            time.sleep(0.02)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,
                                 screen_x, screen_y, 0, 0)

            # restore previous foreground
            if fg_hwnd:
                fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
                user32.AttachThreadInput(self_thread, fg_thread, True)
                try:
                    user32.SetForegroundWindow(fg_hwnd)
                finally:
                    user32.AttachThreadInput(self_thread, fg_thread, False)

            print("sendinput: client({},{}) -> screen({},{})".format(
                client_x, client_y, screen_x, screen_y))
            return True
        except Exception as e:
            print("click_screen_coords failed: {}".format(e))
            return False

    def _bg_click(self, x, y):
        """
        Multi-method bg click dispatcher.
        Converts template-match screenshot coords to the chosen click method.
        """
        if not self._ensure_hwnd():
            print("error: no hwnd, bg click failed")
            return False

        try:
            screen_x, screen_y, logical_x, logical_y, scale = \
                self._get_screen_coords(x, y)

            method = self.click_method.lower() if self.click_method else "postmessage"
            if method == "sendmessage":
                self._bg_click_sendmessage(logical_x, logical_y)
            elif method == "sendinput":
                self._bg_click_sendinput(screen_x, screen_y)
            elif method == "adb":
                self._bg_click_adb(screen_x, screen_y)
            else:  # default: postmessage
                self._bg_click_postmessage(logical_x, logical_y)

            print("bg click: method={} screen({},{}) +offset({},{})"
                  " -> logical({},{}) scale={}".format(
                self.click_method, x, y, self.click_offset_x,
                self.click_offset_y, logical_x, logical_y, scale))

            if self.debug:
                self._debug_mark_click(screen_x, screen_y, logical_x, logical_y)
            return True
        except Exception as e:
            print("bg click failed: {}".format(e))
            return False

    def _debug_mark_click(self, screen_x, screen_y, logical_x=None, logical_y=None):
        """
        Capture the window screenshot, draw crosshairs at both the
        screenshot-space click point and the PostMessage logical coordinate,
        then save to ../games/debug_bg_click.png for verification.
        """
        import os
        try:
            img = self._capture_window()
            if img is None:
                print("debug: screenshot failed, cannot mark click")
                return
            h, w = img.shape[:2]
            thickness = 2
            size = 30

            # --- blue crosshair at screenshot-space click (our intent) ---
            scolor = (255, 0, 0)  # blue
            cv2.line(img,
                     (max(0, int(screen_x) - size), max(0, int(screen_y))),
                     (min(w - 1, int(screen_x) + size), min(h - 1, int(screen_y))),
                     scolor, thickness)
            cv2.line(img,
                     (max(0, int(screen_x)), max(0, int(screen_y) - size)),
                     (min(w - 1, int(screen_x)), min(h - 1, int(screen_y) + size)),
                     scolor, thickness)
            cv2.circle(img, (int(screen_x), int(screen_y)), 8, scolor, 2)
            text = "screen({:.0f},{:.0f})".format(screen_x, screen_y)
            cv2.putText(img, text,
                        (min(int(screen_x) + 15, w - 200),
                         max(int(screen_y) - 15, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, scolor, 2)

            # --- red crosshair at PostMessage logical coord ---
            if logical_x is not None and logical_y is not None:
                lcolor = (0, 0, 255)  # red
                cv2.line(img,
                         (max(0, logical_x - size), max(0, logical_y)),
                         (min(w - 1, logical_x + size), min(h - 1, logical_y)),
                         lcolor, thickness)
                cv2.line(img,
                         (max(0, logical_x), max(0, logical_y - size)),
                         (min(w - 1, logical_x), min(h - 1, logical_y + size)),
                         lcolor, thickness)
                cv2.circle(img, (logical_x, logical_y), 10, lcolor, 2)
                text = "msg({},{})".format(logical_x, logical_y)
                cv2.putText(img, text,
                            (min(logical_x + 15, w - 200),
                             max(logical_y + 25, 35)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, lcolor, 2)
                # arrow from screen to logical
                cv2.arrowedLine(img,
                                (int(screen_x), int(screen_y)),
                                (logical_x, logical_y),
                                (0, 200, 255), 2, tipLength=0.3)

            # --- Y-offset ruler: visualize where +0..+40 click_offset lands ---
            ruler_x = logical_x if logical_x is not None else int(screen_x)
            ruler_base_y = logical_y if logical_y is not None else int(screen_y)
            offsets = [0, 5, 10, 15, 20, 25, 30, 35, 40]
            ruler_colors = [
                (0, 255, 0),      # green    +0
                (80, 255, 0),     # +5
                (0, 255, 255),    # yellow   +10
                (0, 200, 255),    # +15
                (0, 140, 255),    # orange   +20
                (0, 80, 255),     # +25
                (0, 0, 255),      # red      +30
                (140, 0, 255),    # purple   +35
                (255, 0, 255),    # magenta  +40 (known cross-row)
            ]
            cv2.line(img, (ruler_x, 0), (ruler_x, h - 1), (180, 180, 180), 1)
            for off, color in zip(offsets, ruler_colors):
                y_pos = min(h - 1, max(0, ruler_base_y + off))
                half_len = 40
                cv2.line(img,
                         (max(0, ruler_x - half_len), y_pos),
                         (min(w - 1, ruler_x + half_len), y_pos),
                         color, 2)
                cv2.circle(img, (ruler_x, y_pos), 4, color, -1)
                label = "+{}".format(off)
                cv2.putText(img, label,
                            (min(ruler_x + half_len + 5, w - 60), y_pos + 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            
            # put scale info
            scale_text = "scale={}".format(self._dpi_scale)
            cv2.putText(img, scale_text, (10, h - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)

            # save to games/ directory
            save_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "games")
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, "debug_bg_click.png")
            cv2.imwrite(save_path, img)
            print("debug: click screenshot saved -> {}".format(save_path))
            print("debug: legend - blue=screen px, red=PostMessage logical, "
                  "orange=transform")
        except Exception as e:
            print("debug: mark click failed: {}".format(e))

    def _bg_double_click(self, x, y):
        """bg double click"""
        self._bg_click(x, y)
        time.sleep(0.1)
        self._bg_click(x, y)

    def _bg_click_center(self):
        """bg click client center (for firstClickSearch)"""
        if not self._ensure_hwnd():
            return
        try:
            rect = win32gui.GetClientRect(self.hwnd)
            cx = (rect[2] - rect[0]) // 2
            cy = (rect[3] - rect[1]) // 2
            self._bg_click(cx, cy)
        except Exception as e:
            print("bg click center failed: {}".format(e))

    # mapping: friendly key name strings -> win32con VK_xxx integer
    _KEY_NAME_MAP = {
        "esc": win32con.VK_ESCAPE,
        "escape": win32con.VK_ESCAPE,
        "enter": win32con.VK_RETURN,
        "return": win32con.VK_RETURN,
        "space": win32con.VK_SPACE,
        "tab": win32con.VK_TAB,
        "backspace": win32con.VK_BACK,
        "delete": win32con.VK_DELETE,
        "insert": win32con.VK_INSERT,
        "home": win32con.VK_HOME,
        "end": win32con.VK_END,
        "pageup": win32con.VK_PRIOR,
        "pagedown": win32con.VK_NEXT,
        "up": win32con.VK_UP,
        "down": win32con.VK_DOWN,
        "left": win32con.VK_LEFT,
        "right": win32con.VK_RIGHT,
        "f1": win32con.VK_F1,
        "f2": win32con.VK_F2,
        "f3": win32con.VK_F3,
        "f4": win32con.VK_F4,
        "f5": win32con.VK_F5,
        "f6": win32con.VK_F6,
        "f7": win32con.VK_F7,
        "f8": win32con.VK_F8,
        "f9": win32con.VK_F9,
        "f10": win32con.VK_F10,
        "f11": win32con.VK_F11,
        "f12": win32con.VK_F12,
    }

    @classmethod
    def _resolve_vk_code(cls, vk_code):
        """Resolve vk_code to integer VK code.
        Accepts: integer (e.g. 27), "VK_ESCAPE" (win32con attr name),
        or friendly name (e.g. "esc", "escape").
        """
        if isinstance(vk_code, int):
            return vk_code

        # try friendly name map first (case-insensitive)
        key_lower = vk_code.lower()
        if key_lower in cls._KEY_NAME_MAP:
            return cls._KEY_NAME_MAP[key_lower]

        # try win32con attribute lookup (e.g. "VK_ESCAPE" -> 27)
        try:
            code = getattr(win32con, vk_code)
            if isinstance(code, int):
                return code
        except AttributeError:
            pass

        # try with "VK_" prefix if not already present
        if not vk_code.upper().startswith("VK_"):
            try:
                code = getattr(win32con, "VK_" + vk_code.upper())
                if isinstance(code, int):
                    return code
            except AttributeError:
                pass

        # last resort: try ord() for single char keys (e.g. "A" -> 65)
        if len(vk_code) == 1:
            return ord(vk_code.upper())

        print("_bg_press_key: cannot resolve vk_code '{}'".format(vk_code))
        return None

    @staticmethod
    def _make_key_lparam(vk_code, is_keyup=False):
        """Build proper lParam for WM_KEYDOWN/WM_KEYUP messages.

        lParam bit layout:
          0-15:  repeat count (1)
          16-23: scan code (via MapVirtualKey)
          24:    extended key flag (0 or 1)
          25-28: reserved (0)
          29:    context code (1 if ALT pressed, else 0)
          30:    previous key state (0=was up, 1=was down)
          31:    transition state (0=pressing, 1=releasing)
        """
        try:
            scan_code = user32.MapVirtualKeyW(vk_code, 0)  # MAPVK_VK_TO_VSC
        except Exception:
            scan_code = 0
        repeat_count = 1
        lparam = (scan_code << 16) | (repeat_count & 0xFFFF)

        # extended-key flag for certain keys
        extended_keys = {
            win32con.VK_LEFT, win32con.VK_RIGHT, win32con.VK_UP,
            win32con.VK_DOWN,
            win32con.VK_INSERT, win32con.VK_DELETE, win32con.VK_HOME,
            win32con.VK_END, win32con.VK_PRIOR, win32con.VK_NEXT,
            win32con.VK_DIVIDE,  # numpad /
        }
        if vk_code in extended_keys:
            lparam |= (1 << 24)

        if is_keyup:
            lparam |= (1 << 31)   # transition: key going up
            lparam |= (1 << 30)   # previous state: was down

        return lparam

    def _bg_press_key_postmessage(self, code):
        """PostMessage key - async, lightweight. Uses keybd_event to update
        system keyboard state table BEFORE sending window messages, so that
        synchronous WndProc handlers calling GetKeyState/GetAsyncKeyState
        see the correct key state. Scan code from MapVirtualKey for DInput
        compatibility. No SetForegroundWindow needed."""
        lparam_down = self._make_key_lparam(code, is_keyup=False)
        lparam_up = self._make_key_lparam(code, is_keyup=True)
        scan = self._make_key_lparam(code, is_keyup=False) >> 16 & 0xFF
        # 1. Update system keyboard state FIRST (GetAsyncKeyState sees it)
        win32api.keybd_event(code, scan, 0, 0)
        time.sleep(0.01)
        # 2. Send window message (WndProc gets it, sees updated state)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, code, lparam_down)
        time.sleep(0.05)
        # 3. Send window message for key release
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, code, lparam_up)
        # 4. Restore system keyboard state
        win32api.keybd_event(code, scan, win32con.KEYEVENTF_KEYUP, 0)
        return True

    def _bg_press_key_sendmessage(self, code):
        """SendMessage key - sync, finds child window. CRITICAL: keybd_event
        must be called BEFORE SendMessage because SendMessage runs the game's
        WndProc synchronously. If the game checks GetAsyncKeyState during
        WM_KEYDOWN processing, the state must already reflect the key press.
        Scan code from MapVirtualKey for DirectInput compatibility.
        No SetForegroundWindow needed."""
        target_hwnd = self._find_click_target()
        if target_hwnd is None:
            target_hwnd = self.hwnd

        lparam_down = self._make_key_lparam(code, is_keyup=False)
        lparam_up = self._make_key_lparam(code, is_keyup=True)
        scan = (lparam_down >> 16) & 0xFF  # extract scan code from lparam

        def _send_key_cycle(hw):
            # 1. Update system keyboard state FIRST (critical for sync WndProc)
            win32api.keybd_event(code, scan, 0, 0)
            time.sleep(0.01)
            # 2. Send window message (WndProc runs synchronously, sees updated state)
            win32api.SendMessage(hw, win32con.WM_KEYDOWN, code, lparam_down)
            time.sleep(0.05)
            # 3. Send window message for key release
            win32api.SendMessage(hw, win32con.WM_KEYUP, code, lparam_up)
            # 4. Restore system keyboard state
            win32api.keybd_event(code, scan, win32con.KEYEVENTF_KEYUP, 0)

        _send_key_cycle(target_hwnd)
        if target_hwnd != self.hwnd:
            time.sleep(0.03)
            _send_key_cycle(self.hwnd)
        return True

    def _bg_press_key_sendinput(self, code):
        """keybd_event via system input queue with brief foreground activation.
        This is the most reliable method for DirectX games because:
        1. keybd_event updates global keyboard state (GetAsyncKeyState sees it)
        2. Brief SetForegroundWindow ensures the game has input focus
        3. Previous foreground window is restored afterwards
        Same approach as _click_screen_coords.
        """
        try:
            # save & attach for SetForegroundWindow permission
            fg_hwnd = user32.GetForegroundWindow()
            fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None) if fg_hwnd else 0
            self_thread = ctypes.windll.kernel32.GetCurrentThreadId()
            if fg_hwnd and fg_thread:
                user32.AttachThreadInput(self_thread, fg_thread, True)

            try:
                user32.SetForegroundWindow(self.hwnd)
                time.sleep(0.05)
            finally:
                if fg_hwnd and fg_thread:
                    user32.AttachThreadInput(self_thread, fg_thread, False)

            # send key via keybd_event (system queue, updates GetAsyncKeyState)
            win32api.keybd_event(code, 0, 0, 0)           # key down
            time.sleep(0.05)
            win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0)  # key up
            time.sleep(0.02)

            # restore previous foreground window
            if fg_hwnd:
                fg_thread2 = user32.GetWindowThreadProcessId(fg_hwnd, None)
                user32.AttachThreadInput(self_thread, fg_thread2, True)
                try:
                    user32.SetForegroundWindow(fg_hwnd)
                finally:
                    user32.AttachThreadInput(self_thread, fg_thread2, False)

            return True
        except Exception as e:
            print("bg key sendinput failed: {}".format(e))
            return False

    def _bg_press_key(self, vk_code):
        """Multi-method bg key dispatcher, aligned with _bg_click design.

        Dispatch strategy based on self.click_method:
          - "sendmessage": SendMessage to child+parent (no focus change)
          - "sendinput":   keybd_event via system queue, briefly focuses window
          - "postmessage" (default): PostMessage async, lightweight

        vk_code can be:
          - int: raw VK code (e.g. win32con.VK_ESCAPE = 27)
          - str: "VK_ESCAPE" (win32con attribute name)
          - str: friendly name (e.g. "esc", "escape", "enter", "f1")
          - str: single character (e.g. "A", "1")
        """
        if not self._ensure_hwnd():
            print("error: no hwnd, bg key failed")
            return False

        code = self._resolve_vk_code(vk_code)
        if code is None:
            return False

        try:
            method = self.click_method.lower() if self.click_method else "postmessage"
            if method == "sendinput":
                self._bg_press_key_sendinput(code)
            elif method == "sendmessage":
                self._bg_press_key_sendmessage(code)
            else:  # default: postmessage
                self._bg_press_key_postmessage(code)

            print("bg key: {} (VK={}) method={}".format(vk_code, code, method))
            return True
        except Exception as e:
            print("bg key failed: {}".format(e))
            return False

    # ---------- public API ----------

    def writeSelf(self, name, x, y):
        """record image name and match coords"""
        self.name = name
        self.x = x
        self.y = y

    def isVisible(self, name):
        """quick check if template is currently visible (confidence 0.7)"""
        try:
            filepath = path + name + '.png'
            img = dao.my_cv_imread(filepath)
            screenshot = self._capture_window()
            if screenshot is None:
                return False
            result = self._locate_image(img, screenshot, confidence=0.7)
            return result is not None
        except Exception:
            return False

    def waitUntilGone(self, name, timeout=10.0, interval=0.3):
        """Wait until the named template disappears from screen.
        Returns True when gone, False on timeout."""
        start = time.time()
        while time.time() - start < timeout:
            if not self.isVisible(name):
                print("wait: '{}' gone after {:.1f}s".format(
                    name, time.time() - start))
                return True
            time.sleep(interval)
        print("wait: '{}' still visible after {}s timeout".format(name, timeout))
        return False

    def onlySearchOnce(self, name, mode, times):
        """search image once, return 1 found / 0 not found"""
        try:
            filepath = path + name + '.png'
            img = dao.my_cv_imread(filepath)
            screenshot = self._capture_window()
            if screenshot is None:
                return 0
            result = self._locate_image(img, screenshot, confidence=0.7)
            if result is None:
                return 0
            x, y, w, h = result
            center_x = x + w // 2
            center_y = y + h // 2
            self.writeSelf(name, center_x, center_y)
            print("{}.png pos: X={},Y={}, {}x{}px".format(
                name, center_x, center_y, w, h))
            return 1
        except Exception as e:
            return 0

    def loopSearch(self, gamePagesMap):
        """loop search image list, return self on first match"""
        count = 0
        while True:
            for i in gamePagesMap:
                print("----searching: {}".format(i))
                time.sleep(0.2)
                if 0 != self.onlySearchOnce(i, 3, 3):
                    return self
            count += 1
            if count == 5:
                time.sleep(0.1)
                count = 0

    def firstClickSearch(self, gamePagesMap):
        """enter game: loop search, click center if not found"""
        count = 0
        while True:
            for i in gamePagesMap:
                if 0 != self.onlySearchOnce(i, 3, 3):
                    return self
                else:
                    self._bg_click_center()
                    time.sleep(5)
            count += 1
            if count == 5:
                print("5 misses, sleep 0.3s")
                time.sleep(0.3)
                count = 0

    def searchPhoto(self, name):
        """search image until found, grayscale confidence 0.9, exit after 20 fails"""
        count = 0
        found = False
        while not found:
            try:
                filepath = path + name + '.png'
                img = dao.my_cv_imread(filepath)
                screenshot = self._capture_window()
                if screenshot is None:
                    raise Exception("screenshot failed")
                result = self._locate_image(img, screenshot, confidence=0.9,
                                            grayscale=True)
                if result is None:
                    raise Exception("not found")
                x, y, w, h = result
                center_x = x + w // 2
                center_y = y + h // 2
                print("{}.png pos: X={},Y={}, {}x{}px".format(
                    name, center_x, center_y, w, h))
                found = True
                self.writeSelf(name, center_x, center_y)
                return self
            except Exception:
                count = count + 1
                print('{}.png not found, retry #{}, wait 3s'.format(name, count))
                time.sleep(3)
                if count > 20:
                    print("over {} fails, exit".format(count))
                    exit()
