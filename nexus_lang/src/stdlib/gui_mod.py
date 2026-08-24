"""
Sapphire GUI Automation (Mouse, Keyboard, Dialogs) Standard Library
"""
import ctypes
import time
import subprocess
import platform

class GUIModule:
    @staticmethod
    def get_mouse_pos() -> dict:
        """Returns {x, y} mouse cursor position."""
        if platform.system() == "Windows":
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            pt = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            return {"x": pt.x, "y": pt.y}
        return {"x": 0, "y": 0}

    @staticmethod
    def move_mouse(x: int, y: int):
        """Moves mouse cursor to absolute screen coordinates (x, y)."""
        if platform.system() == "Windows":
            ctypes.windll.user32.SetCursorPos(int(x), int(y))

    @staticmethod
    def click(x: int = None, y: int = None):
        """Clicks left mouse button at current position or specified coordinates."""
        if platform.system() == "Windows":
            if x is not None and y is not None:
                ctypes.windll.user32.SetCursorPos(int(x), int(y))
            # MOUSEEVENTF_LEFTDOWN = 0x0002, MOUSEEVENTF_LEFTUP = 0x0004
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            time.sleep(0.05)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)

    @staticmethod
    def right_click(x: int = None, y: int = None):
        """Clicks right mouse button."""
        if platform.system() == "Windows":
            if x is not None and y is not None:
                ctypes.windll.user32.SetCursorPos(int(x), int(y))
            # MOUSEEVENTF_RIGHTDOWN = 0x0008, MOUSEEVENTF_RIGHTUP = 0x0010
            ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
            time.sleep(0.05)
            ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)

    @staticmethod
    def type_text(text: str, interval_ms: int = 10):
        """Simulates typing text string via PowerShell / SendKeys."""
        if platform.system() == "Windows":
            safe_text = str(text).replace('"', '`"').replace('$', '`$')
            ps_script = f'''
            $wshell = New-Object -ComObject wscript.shell;
            $wshell.SendKeys("{safe_text}")
            '''
            subprocess.run(["powershell", "-Command", ps_script])

    @staticmethod
    def press_key(key: str):
        """Simulates key press (e.g. '{ENTER}', '{TAB}', '{ESCAPE}', 'A')."""
        if platform.system() == "Windows":
            ps_script = f'''
            $wshell = New-Object -ComObject wscript.shell;
            $wshell.SendKeys("{key}")
            '''
            subprocess.run(["powershell", "-Command", ps_script])

    @staticmethod
    def alert(message: str, title: str = "Nexus Alert"):
        """Displays GUI Alert Dialog."""
        if platform.system() == "Windows":
            ps_cmd = f'[System.Windows.Forms.MessageBox]::Show("{message}", "{title}")'
            subprocess.run(["powershell", "-Command", f'[reflection.assembly]::loadwithpartialname("System.Windows.Forms"); {ps_cmd}'])
        else:
            print(f"🚨 ALERT [{title}]: {message}")
