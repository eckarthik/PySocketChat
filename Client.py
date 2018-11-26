import socket,threading,random
from tkinter import *
from tkinter import messagebox
socketObj = None
clientName = None
serverPassword = None
connectionDetailsValidationFlag = 0
#GUI

def receiveMessages(serverSocket):
    while True:
        try:
            message = serverSocket.recv(1024).decode("UTF-8")
        except ConnectionResetError as e:
            textBox.config(state=NORMAL)
            textBox.insert(END, "\n" + str(e.strerror))
            textBox.config(state=DISABLED)
            break
        except ConnectionAbortedError as e:
            textBox.config(state=NORMAL)
            textBox.insert(END, "\n" + str(e.strerror))
            textBox.config(state=DISABLED)
            break
        except ConnectionError as e:
            textBox.config(state=NORMAL)
            textBox.insert(END, "\n" + str(e.strerror))
            textBox.config(state=DISABLED)
            break
        else:
            #identify the : character in the message
            index = 0
            for char in message:
                if char==':':
                    break
                else:
                    index+=1
            randNum = random.randrange(1,3)
            tagName = "name"+str(randNum)
            textBox.config(state=NORMAL)
            textBox.insert(END, "\n" + message,tagName)
            textBox.config(state=DISABLED)
            lineCount = str(int(textBox.index('end').split('.')[0])-1)
            #print("Index = ", index, " lineCOunt = ", lineCount,"rand = ",randNum)
            textBox.tag_add("name1",lineCount+".0",lineCount+"."+str(index))
            textBox.tag_config("name1", foreground='red')
            textBox.tag_add("name2", lineCount + ".0", lineCount + "." + str(index))
            textBox.tag_config("name2", foreground='green')
            textBox.tag_add("message", lineCount + "." + str(index), lineCount + "." + str(len(message)))
            textBox.tag_config("message", foreground='black')


def sendMessage():
    #print("Inside send message"+message.get())
    message = messageBox.get("1.0","end-1c")
    global socketObj
    try:
        socketObj.send(message.encode("UTF-8"))
    except ConnectionResetError as e:
        textBox.config(state=NORMAL)
        textBox.insert(END, "\n Unable to send message: " + str(e.strerror))
        textBox.config(state=DISABLED)
    except ConnectionAbortedError as e:
        textBox.config(state=NORMAL)
        textBox.insert(END, "\n Unable to send message: " + str(e.strerror))
        textBox.config(state=DISABLED)
    except ConnectionError as e:
        textBox.config(state=NORMAL)
        textBox.insert(END, "\n Unable to send message: " + str(e.strerror))
        textBox.config(state=DISABLED)
    else:
        messageBox.delete("1.0",END)

def printIP():
    global socketObj
    socketObj = socket.socket()
    port = 10345
    global serverPassword
    serverPassword = passwordFromGUI.get()
    try:
        socketObj.connect((ipAddrFromGUI.get(), port))
    except socket.gaierror:
        #print("Invalid Server address or Server is not alive")
        messagebox.showerror("Error", "Invalid Server address or Server is not alive")
    else:
        print(ipAddrFromGUI.get(),usernameFromGUI.get())
        # clientName = str(input("Choose a name for userself \n"))
        global clientName
        clientName = usernameFromGUI.get()
        socketObj.send(clientName.encode("UTF-8")+":".encode("UTF-8")+serverPassword.encode("UTF-8"))
        validations = str(socketObj.recv(1024).decode("UTF-8"))
        print(validations)
        if validations == "EverythingIsFine":
            threading.Thread(target=receiveMessages, args=(socketObj,)).start()
            window.destroy()
            global connectionDetailsValidationFlag
            connectionDetailsValidationFlag = 1
        elif validations == "IncorrectPassword":
            print("Incorrect Password \n")
            messagebox.showerror("Error","Incorrect Password")
            socketObj.close()
        elif validations == "UsernameAlreadyUsed":
            messagebox.showerror("Error", "Username already used")
            socketObj.close()
window = Tk()
window.geometry('300x200')
window.title("Enter Server Details")
labelIPAddr = Label(window, text="Enter Server IP").pack()
ipAddrFromGUI = StringVar()
entryBoxIPAddr = Entry(window,textvariable=ipAddrFromGUI).pack()
labelServerPassword = Label(window, text="Enter Password").pack()
passwordFromGUI = StringVar()
entryBoxPassword = Entry(window,textvariable=passwordFromGUI).pack()
labelUsername = Label(window, text="Choose a username").pack()
usernameFromGUI = StringVar()
entryBoxUsername = Entry(window, textvariable=usernameFromGUI).pack()
button = Button(window, width=8, height=1, text="Connect", command=printIP, font=('Comic Sans MS', 14, 'bold'),
                relief=RAISED, )
button.pack(pady=15)
window.mainloop()

if connectionDetailsValidationFlag==1:
    mainWindow = Tk()
    mainWindow.title("Chat")
    textBox = Text(mainWindow, height=20, width=50, fg='blue', font=('Comic Sans MS', 12))
    textBox.insert(END, 'Hello ' + clientName)
    textBox.pack()
    # textBox.tag_configure('me',foreground='green')
    label = Label(mainWindow, text="Enter message").pack()
    messageBox = Text(mainWindow, height=5, width=40)
    messageBox.pack()
    button = Button(mainWindow, width=8, height=1, text="Send", command=sendMessage, font=('Comic Sans MS', 14, 'bold'),
                    relief=RAISED, )
    button.pack(pady=15)
    mainWindow.attributes("-topmost", True)
    mainWindow.attributes("-topmost", False)
    mainWindow.mainloop()
    socketObj.close()
else:
    socketObj.close()


