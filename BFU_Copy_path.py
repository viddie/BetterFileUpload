import sys
import pyperclip

def copyTextToClipboard(text):
    pyperclip.copy(text)

if(len(sys.argv) == 2):
    path = sys.argv[1]
    copyTextToClipboard(path)



#"C:\Users\<User>\AppData\Local\Programs\Python\Python36-32\python.exe" "C:\Users\<User>\Desktop\path_to_clipboard.py" "%1"
