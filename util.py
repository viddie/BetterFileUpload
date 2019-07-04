import pyperclip

from win32api import *
from win32gui import *
import win32con
import struct
import time
import os, sys

def formatSizeUnits(bytes):
    if (bytes >= 1073741824):
        bytes = "{:.2f} GB".format(bytes / 1073741824)

    elif (bytes >= 1048576):
        bytes = "{:.2f} MB".format(bytes / 1048576)

    elif (bytes >= 1024):
        bytes = "{:.2f} KB".format(bytes / 1024)

    elif (bytes > 1):
        bytes = bytes + ' bytes'

    elif (bytes == 1):
        bytes = bytes + ' byte'

    else:
        bytes = '0 bytes'

    return bytes

def formatTimeUnits(seconds):
    formatted = ""
    if (seconds >= 86400):
        formatted = str(int(seconds / 86400))
        seconds = '1 day' if formatted == 1 else formatted+' days'

    elif (seconds >= 3600):
        formatted = str(int(seconds / 3600))
        seconds = '1 h' if formatted == 1 else formatted+' h'

    elif (seconds >= 60):
        formatted = str(int(seconds / 60))
        seconds = '1 m' if formatted == 1 else formatted+' m'

    elif (seconds >= 1):
        seconds = "{} s".format(int(seconds))

    else:
        seconds = '0 s'

    return seconds

def copyTextToClipboard(text):
    pyperclip.copy(text)


class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",title,200,msg))
        # self.show_balloon(title, msg)
        time.sleep(5)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.
def balloon_tip(title, msg):
    w=WindowsBalloonTip(msg, title)
