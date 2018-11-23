import tkinter
from tkinter import *
import socket
import threading
socketobj=socket.socket()
socketobj.connect(('172.17.120.59',12345))
mainwindow=tkinter.Tk()      #starting the main window
mainwindow.title('Message me')
textbox=Text(mainwindow)
#textbox.config(state=DISABLED)
textbox.pack()
s=StringVar()
msg=Entry(mainwindow,textvariable=s)
msg.pack()
msg.focus_set()
def recevingthread():
    while True:
        dat=socketobj.recv(1024)
        if dat:
            textbox.insert(INSERT,dat.decode('UTF-8')+'\n')
        else:
            break
def senddata(data):
    socketobj.send(data.encode('UTF-8'))
def adddata():
    data='Deepak:'+msg.get()
    s.set('')
    threading.Thread(target=senddata,args=(data,)).start()
#ADDING BUTTON FOR EXIT AND SEND TEXT
send=tkinter.Button(mainwindow,text='Send',width=30,command=adddata)
send.pack()
button=tkinter.Button(mainwindow,text='Exit',width=30,command=mainwindow.destroy)
button.pack()
threading.Thread(target=recevingthread,args=()).start()
mainwindow.mainloop()   #closing the main window
socketobj.close()