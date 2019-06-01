import winreg
import os
import sys

pythonPath = sys.executable
pythonPath = pythonPath.split(".exe")[0] + "w.exe"

def installEntry(key, scriptPath):
    handle = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key)
    handleCommand = winreg.CreateKey(handle, "command")
    value = "\"{}\" \"{}\" \"%1\"".format(pythonPath, scriptPath)
    winreg.SetValue(handleCommand, "", winreg.REG_SZ, value)

uploadName = "BFU_Upload.py";
uploadDisplayEntry = "BFU - Upload";
copyName = "BFU_Copy_path.py";
copyDisplayEntry = "BFU - Copy path";


pathToFolder = os.path.dirname(os.path.abspath(__file__))
pathToUpload = pathToFolder+"\\"+uploadName
pathToCopy = pathToFolder+"\\"+copyName

keyUpload = "*\\shell\\"+uploadDisplayEntry
keyCopy = "*\\shell\\"+copyDisplayEntry
keyCopyFolder = "Folder\\shell\\"+copyDisplayEntry

installEntry(keyUpload, pathToUpload);
installEntry(keyCopy, pathToCopy);
installEntry(keyCopyFolder, pathToCopy);
