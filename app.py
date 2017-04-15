import os
import time
print 'start'

import subprocess

def interpret(msg):
    msg=msg.lstrip()
    msg=msg.rstrip()
    flag=True
    if msg == 'avrdude: AVR device initialized and ready to accept instructions':
        print 'Me: Device Connected'
    if msg=='avrdude: error: program enable: target doesn\'t answer. 1':
        print 'Me: Error: Check Device'
        flag = False
    if msg=='avrdude: erasing chip':
        print 'Me: Chip Erased'
    if msg=='avrdude: error: could not find USB device with vid=0x16c0 pid=0x5dc vendor=\'www.fischl.de\' product=\'USBasp\'':
        print 'Me: Error: Check Programmer'
        flag = False
    if msg=='Writing |':
        print 'Writing'
    if msg=='Verifying |':
        print 'Verifying'
    return flag

def runProcess(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,bufsize=1)
    line=''
    cnt=0
    while(True):
        retcode = p.poll() #returns None while subprocess is running
##      line = p.stdout.readline()
        c=p.stdout.read(1)
        if c=='#':
            if line != '':
                print line
                # interpret(line)
                line=''
            cnt=cnt+1
            print cnt,
        elif c=='\n':
            print line
            # interpret(line)
            line=''
        else:
            if cnt!=0:
                cnt=0
            line=line+c
        if c=='' and retcode is not None:
            break

##        if(retcode is not None and c=='\n'):
##            break

runProcess('avrdude -C avrdude.conf -p m328p -c usbasp') #Check Device
##runProcess('avrdude -C avrdude.conf -p m328p -c usbasp -e') #Erase
##runProcess('avrdude -C avrdude.conf -p m328p -c usbasp -D -U flash:w:Blink.ino.hex:i') #Write
##runProcess('avrdude -C avrdude.conf -p m328p -c usbasp -D -U lock:w:0x00:m') #Lock

print 'end'
