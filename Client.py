import socket,threading,random
from tkinter import *
def receiveMessages(serverSocket):
    while True:
        message = serverSocket.recv(1024).decode("UTF-8")
        #identify the : character in the message
        index = 0
        for char in message:
            if char==':':
                break
            else:
                index+=1
        randNum = random.randrange(1,3)
        tagName = "name"+str(randNum)
        textBox.insert(END, "\n" + message,tagName)
        lineCount = str(int(textBox.index('end').split('.')[0])-1)
        print("Index = ", index, " lineCOunt = ", lineCount,"rand = ",randNum)
        textBox.tag_add("name1",lineCount+".0",lineCount+"."+str(index))
        textBox.tag_config("name1", foreground='red')
        textBox.tag_add("name2", lineCount + ".0", lineCount + "." + str(index))
        textBox.tag_config("name2", foreground='green')
        textBox.tag_add("message", lineCount + "." + str(index), lineCount + "." + str(len(message)))
        textBox.tag_config("message", foreground='black')


def sendMessage():
    #print("Inside send message"+message.get())
    socketObj.send(message.get().encode("UTF-8"))

socketObj = socket.socket()
port = 10345
clientName = str(input("Choose a name for userself \n"))
socketObj.connect(('127.0.0.1', port))
socketObj.send(clientName.encode("UTF-8"))
threading.Thread(target=receiveMessages, args=(socketObj,)).start()


mainWindow = Tk()
mainWindow.title("Chat")
textBox = Text(mainWindow, height=30, width=50,fg='blue')
textBox.insert(END, 'Hello '+clientName)
textBox.pack()

#textBox.tag_configure('me',foreground='green')
label = Label(mainWindow,text="Enter message").pack()
message = StringVar()
messageBox = Entry(mainWindow,textvariable=message).pack()
button = Button(mainWindow,text="Send",command=sendMessage).pack()
mainWindow.mainloop()


