import tkFileDialog
from Tkinter import *
import subprocess
import ttk
import time
import tkFileDialog

class GUI:

    def getIcCode(self):
        ans=''
        ic=self.var1.get()
        # print ic
        if ic=='ATMEGA328P':
            ans='m328p'
        ans = 'm328p'
        return ans
    def display(self,msg):
        self.text.insert(END,msg)
        self.text.insert(END,'\n')
        self.text.see(END)
    def interpret(self, msg):
        msg = msg.lstrip()
        msg = msg.rstrip()
        print msg
        ans=''
        if msg == 'avrdude: ERROR: No valid record found in Intel Hex file "%s"'%(self.E1.get()):
            ans= 'Invalid File'
            self.f1=0
        if msg == 'avrdude: can\'t open input file : Invalid argument':
            ans= 'Invalid File'
            self.f1=0
        if msg == 'avrdude: error: program enable: target doesn\'t answer. 1':
            ans= 'Error: Check Device'
            self.f1=0
        if msg == 'avrdude: erasing chip':
            ans= 'Chip Erased'
        if msg == 'avrdude: error: could not find USB device with vid=0x16c0 pid=0x5dc vendor=\'www.fischl.de\' product=\'USBasp\'':
            ans= 'Error: Check Programmer'
            self.f1=0
        if msg == 'avrdude: AVR device initialized and ready to accept instructions':
            ans= 'Device Connected'
        if msg == 'avrdude: AVR device initialized and ready to accept instructions':
            ans= 'Device Connected \nReading'
            self.reading.start()
            self.fReading = True
            self.bar=ans
            self.cnt=0
##            self.flag=1
        if msg == 'Writing |':
            ans= 'Writing...'
            self.writing.start()
            self.fWriting = True
            self.bar=ans
            self.cnt = 0
        if msg == 'avrdude: reading on-chip flash data:' or msg == 'avrdude: reading on-chip lock data:' :
            while True:
                if self.p.stdout.read(1) == '#':
                    break
            ans = 'Verifying...'
            self.verifying.start()
            self.fVerifying = True
            self.bar = ans
            self.cnt = 0
        if msg == 'Erasing |':
            ans = 'Erasing...'
            self.erasing.start()
            self.fErasing = True
            self.bar = ans
            self.cnt = 0
        if msg == 'avrdude done.  Thank you.':
            if self.f1 == 1:
                self.display('Done.')
        if not ans == '':
            print ans
            self.display(ans)
        return ans
    def updateProgress(self):
        cnt=self.cnt
        if self.bar == 'Reading':
            self.reading["value"] = cnt
        if self.bar == 'Writing':
            self.writing["value"] = cnt
        if self.bar == 'Verifying':
            self.verifying["value"] = cnt
        if self.bar == 'Erasing':
            self.verifying["value"] = cnt
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
    def runProcess(self,exe):
        self.p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, bufsize=1)
        self.f1=1
        self.fReading = False
        self.fWriting = False
        self.fVerifying = False
        self.fErasing = False
        self.reading["value"]=0
        self.writing["value"]=0
        self.verifying["value"]=0
        self.bar = ''
        line = ''
        self.cnt = 0
        self.statusBar.config(text="Programmer Busy",bg="#cc0605",width=88) #Status Red
        while (True):
            retcode = self.p.poll()  # returns None while subprocess is running
            c = self.p.stdout.read(1)
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
        self.statusBar.config(text="Programmer Ready",bg="#308446") #Status Green

    
    ##        if(retcode is not None and c=='\n'):
    ##            break

    def helloCallBack(self):
        pass
        # tkMessageBox.showinfo( "Hello Python", "Hello World")
    def donothing(self):
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()
    def openFile(self):
        file_path = tkFileDialog.askopenfilename()
        self.E1.delete(0, END)
        self.E1.insert(0, file_path)
    def erase(self):
        ic=self.getIcCode()
        self.runProcess('avrdude\\avrdude -C avrdude\\avrdude.conf -p %s -c usbasp -e'%(ic)) #Erase
    def lock(self):
        ic=self.getIcCode()
        self.runProcess('avrdude\\avrdude -C avrdude\\avrdude.conf -p %s -c usbasp -D -U lock:w:0x00:m'%(ic)) #Lock    
    def init(self):
        ic=self.getIcCode()
        self.runProcess('avrdude\\avrdude -C avrdude\\avrdude.conf -p %s -c usbasp -D -U efuse:w:0xfd:m'%(ic)) #eFuse    
        self.runProcess('avrdude\\avrdude -C avrdude\\avrdude.conf -p %s -c usbasp -D -U hfuse:w:0xde:m'%(ic)) #hfuse    
        self.runProcess('avrdude\\avrdude -C avrdude\\avrdude.conf -p %s -c usbasp -D -U lfuse:w:0xff:m'%(ic)) #lFuse    
    def write(self):
        ic=self.getIcCode()
        file_path=self.E1.get()
        print file_path
        f1=0
        for i in range(0,len(file_path)):
            c=file_path[len(file_path)-i-1]
            if c=='/':
                f1=len(file_path)-1-i
                break
        file_name=file_path[f1+1:len(file_path)]
        msg='File: %s'%file_name
        if not file_name == '':
            self.display(msg)
        pass
        self.runProcess('avrdude\\avrdude -C avrdude\\avrdude.conf -p %s -c usbasp -D -U flash:w:%s:i'%(ic,file_path)) #Write
    def auto(self):
        self.check()
        if self.f1 == 1 :
            self.erase()
            if self.f1 == 1:
                self.init()
                if self.f1 == 1:
                    self.write()
                    if self.f1 == 1:
                        self.lock()
        if self.f1 == 1:
            self.display('Auto Process Complete')
        else:
            self.display('Auto Process Error')
##        self.runProcess('avrdude -C avrdude.conf -p %s -c usbasp'%(ic)) # Check Device
##        self.runProcess('avrdude -C avrdude.conf -p %s -c usbasp -e'%(ic)) #Erase
##        self.runProcess('avrdude -C avrdude.conf -p %s -c usbasp -D -U lock:w:0x00:m'%(ic)) #Write    
##        self.runProcess('avrdude -C avrdude.conf -p %s -c usbasp -D -U lock:w:0x00:m'%(ic)) #Write            
    def check(self):
        ic=self.getIcCode()
        self.runProcess('avrdude\\avrdude -C avrdude\\avrdude.conf -p %s -c usbasp'%(ic)) # Check Device
        if self.f1 == 1:
            self.display('IC Check Complete')
            self.display('Initializing IC')
            self.init()
            self.display('IC Initialized')
    def createMenu(self,master):
        self.frame = Frame(master)
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="Exit", command=self.frame.quit)
        menubar.add_cascade(label="File", menu=filemenu)
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
##        master.geometry('{}x{}'.format(620, 300))

        row=0

        #Controller
        f0 = Frame(master)
        f0.grid(row=row,sticky=W)
        L0 = Label(f0, text="Select IC: ")
        # L0.grid(row=0, column=0, padx=20, pady=10)
        lst1 = ['ATMEGA328P', 'Option2', 'Option3']
        self.var1 = StringVar(f0)
        self.var1.set(lst1[0])
        # drop = OptionMenu(f0, self.var1, *lst1)
        # drop.grid(column=1,row=0,padx=10)
        row+=1

        #Entry
        f1=Frame(master)
        f1.grid(row=row)
        L1 = Label(f1, text="Hex File:")
        L1.grid(row=0,column=1,padx=20,pady=30)
        self.E1 = Entry(f1, bd =5,width=40)
        self.E1.grid(row=0,column=2,sticky=E+W,columnspan=3,padx=20,pady=0)
        openButton = Button(f1, text ="Browse...", command = self.openFile,width=10)
        openButton.grid(row=0,column=5)
        
        # Button
        # f2=Frame(master)
        # f2.grid(row=1,pady=10)
        C = Button(f1, text="Write", command=self.write,width=10)
        D = Button(f1, text="Initialize", command=self.init,width=10)
        B = Button(f1, text ="Lock", command = self.lock,width=10)
        buttErase = Button(f1, text="Erase", command=self.erase,width=10)
        buttAuto = Button(f1, text="Auto", command=self.auto,width=10)
        buttAuto.grid(row=1,column=1,padx=10)
        D.grid(row=1,column=3,padx=10)
        buttErase.grid(row=1,column=2,padx=10)
        C.grid(row=1,column=4,padx=10)
        B.grid(row=1,column=5,padx=10,pady=0)
        self.statusBar=Label(f1,text="Programmer Ready",bg="#308446",width=88,fg="#ffffff") #Status Green
##        self.statusBar=Label(f1,text="Programmer Busy",bg="#cc0605",width=88,fg="#ffffff",height=1) #Status Red
        self.statusBar.grid(row=2,column=0, columnspan=7,pady=20)
        row+=1
        

        # Verbose
        f3=Frame(master)
        f3.grid(row=row,padx=10,pady=0)
        labelRead=Label(f3,text="Read")
        labelRead.grid(row=0,column=0)
        self.reading = ttk.Progressbar(f3,orient=HORIZONTAL, length=200, mode='determinate')
        self.reading.grid(row=0,column=1,padx=20,pady=0)
        self.reading["maximum"]=50
        labelWrite=Label(f3,text="Write")
        labelWrite.grid(row=1,column=0)
        self.writing = ttk.Progressbar(f3,orient=HORIZONTAL, length=200, mode='determinate')
        self.writing["maximum"]=50
        self.writing.grid(row=1,column=1,padx=20,pady=0)
        labelVerify=Label(f3,text="Verify")
        labelVerify.grid(row=2,column=0)
        self.verifying = ttk.Progressbar(f3,orient=HORIZONTAL, length=200, mode='determinate')
        self.verifying["maximum"]=50
        self.verifying.grid(row=2,column=1,padx=20,pady=0)

        fText=Frame(f3)
        fText.grid(row=0,rowspan=3,column=2,padx=20)
        textY = Scrollbar(fText)
        self.text=Text(fText,width=30,height=5)
        self.text.config(yscrollcommand=textY.set)
        textY.config(command=self.text.yview)
        # textX.config(command=self.text.xview)
        self.text.grid(row=0,column=0)
        textY.grid(row=0, column=1, sticky=N + S)
        # textX.grid(row=1, column=0, sticky=E + W)
        row+=1
        
        # Footer
        f4 = Frame(master)
        text2 = Label(f4,height=1)
        text2.grid(row=0)
        f4.grid(row=row)

root = Tk()
root.title('AVR Uploader v2.3')
b=GUI(root)
root.mainloop()

