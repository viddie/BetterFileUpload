import sys, os
import requests
import util
from util import settings

from tkinter import Tk, HORIZONTAL, StringVar, Label
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar
import time
import threading
import json
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

import traceback


class MonApp(Tk):
    def __init__(self, path):
        super().__init__()

        self.title("Uploading "+path.split("\\")[-1])

        self.row = 1
        self.path = path


        self.lbByteSep = Label(self, text="Loaded:")
        self.lbByteSep.grid(row=self.row, column=0)

        self.byteVar = StringVar()
        self.lbByteProgress = Label(self, textvariable=self.byteVar)
        self.lbByteProgress.grid(row=self.row, column=1)

        self.row += 1

        self.speedVar = StringVar()
        self.lbSpeedProgress = Label(self, textvariable=self.speedVar)
        self.lbSpeedProgress.grid(row=self.row, column=0)

        self.timeLeftVar = StringVar()
        self.lbTimeLeftProgress = Label(self, textvariable=self.timeLeftVar)
        self.lbTimeLeftProgress.grid(row=self.row, column=1)

        self.row += 1

        self.progressBar = Progressbar(self, orient=HORIZONTAL, length=400,  mode='determinate')

        self.lastTime = time.time()
        self.lastLoaded = 0
        self.avgTimeLeft = []
        self.avgCount = 5

        self.startUpload()


    def startUpload(self):
        def real_startUpload():
            def progress(monitor):
                current = monitor.bytes_read
                max = monitor.len
                percent = (current / max) * 100

                currentTime = time.time()
                timeDiff = currentTime - self.lastTime
                if(timeDiff > 1):
                    diffLoaded = current - self.lastLoaded
                    uploadSpeedPerSecond = diffLoaded / timeDiff
                    diffNeeded = max - current
                    secondsLeft = diffNeeded / uploadSpeedPerSecond

                    if(len(self.avgTimeLeft) == self.avgCount):
                        self.avgTimeLeft.pop(0)

                    self.avgTimeLeft.append(secondsLeft)

                    average = secondsLeft if len(self.avgTimeLeft) <= self.avgCount else sum(self.avgTimeLeft) / len(self.avgTimeLeft)

                    self.byteVar.set("{} / {}".format(util.formatSizeUnits(current), util.formatSizeUnits(max)))
                    self.speedVar.set("Speed: {}/s".format(util.formatSizeUnits(uploadSpeedPerSecond)))
                    self.timeLeftVar.set("Time left: "+util.formatTimeUnits(average))

                    self.lastTime = currentTime
                    self.lastLoaded = current

                print("Progress: {} / {} --- {:.1f}%".format(current, max, percent))
                self.progressBar['value'] = percent

            self.progressBar.grid(row=0, column=0, columnspan=2)


            url = settings['upload_url']
            params = {"key": settings['key'], "result_as": "json"}
            filename = self.path.split("\\")[-1]
            filename = filename.encode("ascii", errors="ignore").decode()
            fields = {"file": (filename, open(self.path, 'rb').read())}

            encoder = MultipartEncoder(fields=fields)
            encoderMonitor = MultipartEncoderMonitor(encoder, progress)

            headers = {
                "Connection": "Keep-Alive",
                "Content-Type": encoderMonitor.content_type,
                "Keep-Alive": "timeout=7200"
            }

            response = requests.post(url, data=encoderMonitor, headers=headers, params=params)
            print("Reponse: {}".format(response.text));
            parseResponse(response.text)

            os._exit(0)


        threading.Thread(target=real_startUpload).start()




def displayNotification(title, text):
    util.balloon_tip(title, text)

def uploadFile(path):
    url = settings['upload_url']
    params = {"key": settings['key'], "result_as": "json"}
    filename = path.split("\\")[-1]
    filename = filename.encode("ascii", errors="ignore").decode()
    fields = {"file": (filename, open(path, 'rb').read())}

    encoder = MultipartEncoder(fields=fields)
    encoderMonitor = MultipartEncoderMonitor(encoder, None)

    headers = {
        "Connection": "Keep-Alive",
        "Content-Type": encoderMonitor.content_type,
        "Keep-Alive": "timeout=7200"
    }

    response = requests.post(url, data=encoderMonitor, headers=headers, params=params)

    return response.text

def parseResponse(response):
    response = json.loads(response)
    if(response['errorCode'] == "OK"):
        token = response['token']
        link = settings['download_url'].format(token)
        util.copyTextToClipboard(link)
        displayNotification("Upload done", response['filename']+": "+link)
    else:
        displayNotification("Error", "Error while uploading: "+response['errorMessage'])
        pass

# sys.argv.append("C:\\Users\\viddie\\Downloads\\ES-2019-10-ImplementierungStandards.pdf")
try:
    if(len(sys.argv) == 1):
        Tk().withdraw()
        path = askopenfilename()
        if(path != ""):
            response = uploadFile(path)
            parseResponse(response)
    else:
        path = sys.argv[1]
        threshold = settings['progressBarMBThreshold']
        if(os.path.getsize(path) > threshold*1024*1024):
            app = MonApp(path)
            app.mainloop()
        else:
            response = uploadFile(path)
            parseResponse(response)
except Exception as err:
    traceback.print_exc()
    input()


#"C:\Users\<User>\AppData\Local\Programs\Python\Python36-32\python.exe" "C:\Users\<User>\Desktop\BFU_Upload.py" "%1"
