class A:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
    def seta(self):
        def afunction():
            self.a = 2
        afunction()
    def geta(self):
        return self.a

cA = A()
print cA.a
cA.seta()
print cA.a
print cA.geta()

import tkFileDialog
from Tkinter import *
import subprocess
import ttk
import time

# class GUI:
#
#     def __init__(self,master):
#         # Button
#         f2=Frame(master)
#         # f2.pack(side=TOP)
#         f2.grid(row=2)
#         B = Button(f2, text ="Read")
#         C = Button(f2, text="Write")
#         D = Button(f2, text="Check")
#         buttErase = Button(f2, text="Erase")
#         # D.pack(side=LEFT)
#         # B.pack(side=LEFT)
#         # C.pack(side=LEFT)
#         D.grid(row=1)
#         B.grid(row=2)
#         C.grid(row=3)
#
#         f3=Frame(master)
#         # f2.pack(side=TOP)
#         f3.grid(row=1)
#         B1 = Button(f3, text ="Read1")
#         C1 = Button(f3, text="Write1")
#         D1 = Button(f3, text="Check1")
#         buttErase = Button(f3, text="Erase")
#         # D.pack(side=LEFT)
#         # B.pack(side=LEFT)
#         # C.pack(side=LEFT)
#         D1.grid(row=3)
#         B1.grid(row=2)
#         C1.grid(row=1)
#
#
#
# root = Tk()
# b=GUI(root)
# root.mainloop()

from Tkinter import *

master = Tk()

var = StringVar(master)
var.set("one") # initial value

option = OptionMenu(master, var, "one", "two", "three", "four")
option.pack()

#
# test stuff

def ok():
    print "value is", var.get()
    master.quit()

button = Button(master, text="OK", command=ok)
button.pack()

mainloop()