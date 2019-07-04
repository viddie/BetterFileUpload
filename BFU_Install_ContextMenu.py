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
uploadExtendedName = "BFU_Upload_Extended.py";
uploadExtendedDisplayEntry = "BFU - Upload...";
copyName = "BFU_Copy_path.py";
copyDisplayEntry = "BFU - Copy path";


pathToFolder = os.path.dirname(os.path.abspath(__file__))
pathToUpload = pathToFolder+"\\"+uploadName
pathToUploadExtend = pathToFolder+"\\"+uploadExtendedName
pathToCopy = pathToFolder+"\\"+copyName

keyUpload = "*\\shell\\"+uploadDisplayEntry
keyUploadExtend = "*\\shell\\"+uploadExtendedDisplayEntry
keyCopy = "*\\shell\\"+copyDisplayEntry
keyCopyFolder = "Folder\\shell\\"+copyDisplayEntry

try:
    installEntry(keyUpload, pathToUpload)
    installEntry(keyUploadExtend, pathToUploadExtend)
    installEntry(keyCopy, pathToCopy)
    installEntry(keyCopyFolder, pathToCopy)
except PermissionError as e:
    print("======== ERROR ========")
    print("A permission error occurred.")
    print("Please start the installation as administrator")
    print("=======================")
