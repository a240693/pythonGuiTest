import time
import cv2
import ctypes
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
    def __init__(self, window_title=None):
        """
        bg Photo: bg screenshot + template match + PostMessage bg click.
        API compatible with multiphotos.Photo.

        :param window_title: fuzzy match window by title/class/process
                              read from changeVar, fallback "SDgundam"
                              use Photo.list_windows() to discover
        """
        self.name = "default"
        self.x = 0
        self.y = 0
        self.hwnd = None
        self.process_name = ""
        global path
        path = cv.get_value("path")
        if window_title is None:
            try:
                window_title = cv.get_value("window_title")
            except Exception:
                window_title = "SDgundam"
        self.window_title = window_title
        self._refresh_hwnd()

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
        flag=0 (PW_CLIENTONLY) ensures coordinate match with PostMessage.
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

            # flag=0: PW_CLIENTONLY
            result = user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 0)

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

    def _bg_click(self, x, y):
        """
        PostMessage bg click (client coords), no real mouse.
        Both screenshot and click use client coords (PrintWindow flag=0 + DPI aware).
        """
        if not self._ensure_hwnd():
            print("error: no hwnd, bg click failed")
            return False

        try:
            lparam = win32api.MAKELONG(x, y)
            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                 win32con.MK_LBUTTON, lparam)
            time.sleep(0.05)
            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lparam)
            print("bg click: ({}, {})".format(x, y))
            return True
        except Exception as e:
            print("bg click failed: {}".format(e))
            return False

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

    def _bg_press_key(self, vk_code):
        """PostMessage bg key (VK), no real keyboard"""
        if not self._ensure_hwnd():
            print("error: no hwnd, bg key failed")
            return False

        try:
            lparam = win32api.MAKELONG(0, 0)
            win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code, lparam)
            time.sleep(0.05)
            win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, vk_code, lparam)
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

    def onlySearchOnce(self, name, mode, times):
        """search image once, return 1 found / 0 not found"""
        try:
            filepath = path + name + '.png'
            img = dao.my_cv_imread(filepath)
            screenshot = self._capture_window()
            if screenshot is None:
                return 0
            result = self._locate_image(img, screenshot, confidence=0.8)
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
