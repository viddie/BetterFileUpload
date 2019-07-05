import requests, json, os, sys
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from tkinter import Button, Text, Label, StringVar, Entry, OptionMenu, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
import time
import threading

import util
from util import settings


class MonApp(Tk):
    def __init__(self, path):
        super().__init__()

        self.title("Uploading "+path.split("\\")[-1])

        self.row = 0
        self.path = path

        self.lbCurrentName = Label(self, text="File:")
        self.lbCurrentName.grid(row=self.row, column=0)

        self.tfCurrentName = Label(self, text=path)
        self.tfCurrentName.grid(row=self.row, column=1)
        self.row += 1

        self.lbNewName = Label(self, text="New Name: ")
        self.lbNewName.grid(row=self.row, column=0)

        self.tfNewName = Text(self, height=1, width=30)
        self.tfNewName.grid(row=self.row, column=1)
        self.row += 1

        self.lbPassword = Label(self, text="Password: ")
        self.lbPassword.grid(row=self.row, column=0)

        self.tfPassword = Text(self, height=1, width=30)
        self.tfPassword.grid(row=self.row, column=1)
        self.row += 1

        self.lbVisibility = Label(self, text="Visibility: ")
        self.lbVisibility.grid(row=self.row, column=0)

        self.selVar = StringVar(self)
        self.selVar.set("Public")
        self.selVisibility = OptionMenu(self, self.selVar, "Public", "Member Only", "Private")
        self.selVisibility.grid(row=self.row, column=1)
        self.row += 1

        self.uploadButton = Button(self, text='Start Upload', command=self.startUpload)
        self.uploadButton.grid(row=self.row, column=0)
        self.row += 1



        self.lbByteSep = Label(self, text="Loaded:")
        self.byteVar = StringVar()
        self.lbByteProgress = Label(self, textvariable=self.byteVar)

        self.speedVar = StringVar()
        self.lbSpeedProgress = Label(self, textvariable=self.speedVar)

        self.timeLeftVar = StringVar()
        self.lbTimeLeftProgress = Label(self, textvariable=self.timeLeftVar)

        self.lastTime = time.time()
        self.lastLoaded = 0
        self.avgTimeLeft = []
        self.avgCount = 5


        self.progressBar = Progressbar(self, orient=HORIZONTAL,length=200,  mode='determinate')


        self.lbResultText = Label(self, text="Link: ")
        self.varResultText = StringVar()
        self.entryResultText = Entry(self, textvariable=self.varResultText, width=40)

    def displayResult(self, code, message):
        self.lbResultText['text'] = code
        self.lbResultText.grid(row=7, column=0)

        self.entryResultText.delete(0, "end")
        self.entryResultText.insert(0, message)
        self.entryResultText.grid(row=7, column=1)

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
                    self.speedVar.set("{}/s".format(util.formatSizeUnits(uploadSpeedPerSecond)))
                    self.timeLeftVar.set("Time left: "+util.formatTimeUnits(average))

                    self.lastTime = currentTime
                    self.lastLoaded = current

                print("Progress: {} / {} --- {:.1f}%".format(current, max, percent))
                self.progressBar['value'] = percent

            self.progressBar.grid(row=4, column=1)

            self.lbByteSep.grid(row=5, column=0)
            self.lbByteProgress.grid(row=5, column=1)
            self.lbSpeedProgress.grid(row=6, column=0)
            self.lbTimeLeftProgress.grid(row=6, column=1)



            url = settings['upload_url']
            params = {"key": settings['key'], "result_as": "json"}
            filename = self.path.split("\\")[-1]
            filename = filename.encode("ascii", errors="ignore").decode()
            fields = {"file": (filename, open(self.path, 'rb').read())}

            if(self.tfNewName.get("1.0", "end").strip() != ""):
                fields["newName"] = self.tfNewName.get("1.0", "end-1c")

            if(self.tfPassword.get("1.0", "end").strip() != ""):
                fields["password"] = self.tfPassword.get("1.0", 'end-1c')

            if(self.selVar.get() == "Public"):
                fields["visibility"] = "0"
            elif(self.selVar.get() == "Member Only"):
                fields["visibility"] = "1"
            elif(self.selVar.get() == "Private"):
                fields["visibility"] = "2"

            encoder = MultipartEncoder(fields=fields)
            encoderMonitor = MultipartEncoderMonitor(encoder, progress)

            headers = {
                "Connection": "Keep-Alive",
                "Content-Type": encoderMonitor.content_type,
                "Keep-Alive": "timeout=7200"
            }

            r = requests.post(url, data=encoderMonitor, headers=headers, params=params)
            print("Reponse: {}".format(r.text));

            response = json.loads(r.text)
            if(response['errorCode'] == "OK"):
                token = response['token']
                link = settings['download_url'].format(token)
                util.copyTextToClipboard(link)
                self.displayResult("Link:", link)
            else:
                self.displayResult("Error:", response['errorMessage'])
                pass


        self.uploadButton['state']='disabled'
        threading.Thread(target=real_startUpload).start()


# sys.argv.append("C:\\Users\\viddie\\Downloads\\ES-2019-10-ImplementierungStandards.pdf")
try:
    if(len(sys.argv) == 1):
        app = MonApp("README.md")
        app.mainloop()
    else:
        path = sys.argv[1]
        app = MonApp(path)
        app.mainloop()
except Exception as err:
    traceback.print_exc()
    input()
