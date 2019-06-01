import sys, os
import requests
import pyperclip
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json
from win32api import *
from win32gui import *
import win32con
import struct
import time

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
        time.sleep(10)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.
def balloon_tip(title, msg):
    w=WindowsBalloonTip(msg, title)



settings = {}

def initSettings(path):
    settings['key'] = "Y9V26iHy3OmTKIgUjMcL74GEsBNpJ1Dv"
    settings['upload_url'] = "https://file-upload.vi-home.de/process_upload.php"
    settings['download_url'] = "https://file-upload.vi-home.de/download.php?fid={}"
    settings['direct_url'] = "https://file-upload.vi-home.de/direct.php?fid={}"

    saveSettings(path)

def loadSettings(path):
    global settings

    try:
        open(path, "r")
    except:
        initSettings(path)
        return

    with open(path, "r") as f:
        line = f.readline()
        settings = json.loads(line)

def saveSettings(path):
    with open(path, "w") as f:
        f.write(json.dumps(settings))

def copyTextToClipboard(text):
    pyperclip.copy(text)

def displayNotification(title, text):
    balloon_tip(title, text)

def uploadFile(path):
    params = {"key": settings['key'], "result_as": "json"}
    files = {"file": open(path, 'rb')}
    r = requests.post(settings['upload_url'], params=params, files=files)
    return r.text

# key = "*\shell\SomeKeyName"
# handle = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key)

def parseResponse(response):
    response = json.loads(response)
    if(response['errorCode'] == "OK"):
        token = response['token']
        link = settings['download_url'].format(token)
        copyTextToClipboard(link)
        displayNotification("Upload done", response['filename']+": "+link)
    else:
        displayNotification("Error", "Error while uploading: "+response['errorMessage'])
        pass


loadSettings(os.path.dirname(os.path.abspath(__file__))+"\\settings.txt")

if(len(sys.argv) == 1):
    Tk().withdraw()
    path = askopenfilename()
    if(path != ""):
        response = uploadFile(path)
        parseResponse(response)
else:
    path = sys.argv[1]
    response = uploadFile(path)
    parseResponse(response)



#"C:\Users\viddie\AppData\Local\Programs\Python\Python36-32\python.exe" "C:\Users\viddie\Desktop\BFU_Upload.py" "%1"
