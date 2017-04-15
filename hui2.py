import tkFileDialog
from Tkinter import *
import subprocess
import ttk
import time

class GUI:

    def interpret(self, msg):
        msg = msg.lstrip()
        msg = msg.rstrip()
        print msg
        ans=''
        flag = 'OK'
        if msg == 'avrdude: AVR device initialized and ready to accept instructions':
            ans= 'Me: Device Connected'
        if msg == 'avrdude: error: program enable: target doesn\'t answer. 1':
            ans= 'Me: Error: Check Device'
        if msg == 'avrdude: erasing chip':
            ans= 'Me: Chip Erased'
        if msg == 'avrdude: error: could not find USB device with vid=0x16c0 pid=0x5dc vendor=\'www.fischl.de\' product=\'USBasp\'':
            ans= 'Me: Error: Check Programmer'
        if msg == 'Reading |':
            ans= 'Reading'
            self.reading.start()
            self.fReading = True
            self.bar=ans
            self.cnt=0
        if msg == 'Writing |':
            ans= 'Writing'
            self.writing.start()
            self.fWriting = True
            self.bar=ans
            self.cnt = 0
        if msg == 'Verifying |':
            ans = 'Verifying'
            self.verifying.start()
            self.fVerifying = True
            self.bar = ans
            self.cnt = 0
        if msg == 'Erasing |':
            ans = 'Erasing'
            self.erasing.start()
            self.fErasing = True
            self.bar = ans
            self.cnt = 0
        print ans
        return ans
    def updateProgress(self):
        cnt=self.cnt
        if self.bar == 'Reading':
            self.reading["value"] = cnt
            # self.frame.update_idletasks()
        if self.bar == 'Writing':
            self.writing["value"] = cnt
            # self.frame.update_idletasks()
        if self.bar == 'Verifying':
            self.verifying["value"] = cnt
            # self.frame.update_idletasks()
        if self.bar == 'Erasing':
            self.verifying["value"] = cnt
            # self.frame.update_idletasks()
        if cnt == -1:
            if self.fReading == True:
                self.reading.stop()
                self.reading["value"] = 50
            if self.fWriting == True:
                self.writing.stop()
                self.writing["value"] = 50
            if self.fErasing == True:
                self.erasing.stop()
                self.erasing["value"] = 50
            if self.fVerifying == True:
                self.verifying.stop()
                self.verifying["value"] = 50
        self.frame.update()
        # self.frame.update_idletasks();
    def runProcess(self,exe):
        p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, bufsize=1)
        line = ''
        self.cnt = 0
        while (True):
            retcode = p.poll()  # returns None while subprocess is running
            c = p.stdout.read(1)
            if c == '#':
                if line != '':
                    ##                print line
                    self.interpret(line)
                    line = ''
                    # self.reading.start()
                    # fReading=True
                self.cnt = self.cnt + 1
                self.updateProgress()
                print self.cnt,
                time.sleep(0.01)
            elif c == '\n':
                ##            print line
                self.interpret(line)
                self.cnt=-1
                self.updateProgress()
                # root.after_idle(self.updateProgress)
                line = ''
            else:
                self.cnt=-1
                self.updateProgress()
                if self.cnt != 0:
                    self.cnt = 0
                line = line + c
            if c == '' and retcode is not None:
                break

    ##        if(retcode is not None and c=='\n'):
    ##            break

    def helloCallBack(self):
        pass
        # tkMessageBox.showinfo( "Hello Python", "Hello World")
    def donothing(self):
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()
    def read(self):
        pass
    def erase(self):
        self.runProcess('avrdude -C avrdude.conf -p m328p -c usbasp -e') #Erase
    def write(self):
        file_path=self.E1.get()

        print file_path
        self.runProcess('avrdude -C avrdude.conf -p m328p -c usbasp -D -U flash:w:Blink.ino.hex:i') #Write

    def openFile(self):
        global E1
        file_path = tkFileDialog.askopenfilename()
        E1.insert(0, file_path)
        # print file_path
    def check(self):
        self.runProcess('avrdude -C avrdude.conf -p m328p -c usbasp')  # Check Device
    def createMenu(self,master):
        self.frame = Frame(master)
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.frame.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)

    def __init__(self,master):
        # master=
        # master.minsize(width=480, height=340)
        self.fReading=False
        self.fWriting=False
        self.fVerifying=False
        self.fErasing = False
        self.bar=''
        self.createMenu(master)
        master.geometry('{}x{}'.format(400, 300))

        #Entry
        f1=Frame(master)
        f1.pack(side=TOP)
        L1 = Label(f1, text="Hex File")
        L1.pack( side = LEFT)
        self.E1 = Entry(f1, bd =5,width=50)
        self.E1.pack(side = LEFT)
        openButton = Button(f1, text ="Open", command = self.openFile)
        openButton.pack(side=LEFT)

        # Button
        f2=Frame(master)
        f2.pack(side=TOP)
        B = Button(f2, text ="Read", command = self.read)
        C = Button(f2, text="Write", command=self.write)
        D = Button(f2, text="Check", command=self.check)
        buttErase = Button(f2, text="Erase", command=self.erase)
        D.pack(side=LEFT)
        B.pack(side=LEFT)
        C.pack(side=LEFT)
        buttErase.pack(side=LEFT)

        # Verbose
        f3=Frame(master)
        self.reading = ttk.Progressbar(f3,orient=HORIZONTAL, length=200, mode='determinate')
        self.reading.pack(side="bottom")
        self.reading["maximum"]=50
        self.writing = ttk.Progressbar(f3,orient=HORIZONTAL, length=200, mode='determinate')
        self.writing.pack(side="bottom")
        self.writing["maximum"]=50
        self.verifying = ttk.Progressbar(f3,orient=HORIZONTAL, length=200, mode='determinate')
        self.verifying.pack(side="bottom")
        self.verifying["maximum"]=50
        self.reading.pack(side=TOP,fill=X)
        self.writing.pack(side=TOP,fill=X)
        self.verifying.pack(side=TOP,fill=X)
        # self.progressbar.start()

        f3.pack(side=TOP)
        s3y=Scrollbar(f3)
        s3y.pack(side=RIGHT,fill=Y)
        s3x=Scrollbar(f3,orient=HORIZONTAL)
        s3x.pack(side=BOTTOM,fill=X)
        text = Text(f3,height=7,yscrollcommand=s3y.set,xscrollcommand=s3x.set)
        text.pack()

        # Footer
        f4 = Frame(master)
        f4.pack(side=TOP)
        text2 = Text(f4,height=10)
        text2.pack()

root = Tk()
b=GUI(root)
root.mainloop()

