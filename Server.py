import socket,threading,random
from tkinter import *

socketObj = socket.socket()

socketObj.bind(('',10345))

socketObj.listen(6)
addresses = []
clientNames = []
clientSockets = []
serverPassword = str(random.randrange(100000, 999999))
print("Password = " + str(serverPassword))
window = Tk()
window.title("Monitor Chats")
chatLogsTextBox = Text(window, height=20, width=50, fg='blue', font=('Comic Sans MS', 12))
chatLogsTextBox.pack()
def broadCast(message,isPrivate=False):
    #print("Inside broadcast")
    #chatLogsTextBox.insert(END,"\n Inside broadcast")
    if isPrivate:
        user = message.split(":")[0]
        action = message.split(":")[1].split(" ")[0]
        messageToBeSent = message.split(":")[1].split(" ", 1)[1]
        print("user = ", user)
        print("action = ", action)
        print("message = ", messageToBeSent)
        privateClientName = message.split(":")[1].split(" ")[1]
        print("privateClientName = ",privateClientName)
        if action=="@private":
            for client in clientSockets:
                if client['clientName']==privateClientName.lower():
                    client['socket'].send(str("Private message from "+user+":"+messageToBeSent).encode("UTF-8"))
                    for client2 in clientSockets:
                        if client2['clientName'] == user:
                            client2['socket'].send(str("Private message sent to " + privateClientName).encode("UTF-8"))
    else:
        for client in clientSockets:
            client['socket'].send(message.encode("UTF-8"))

def handleClient(socket,clientName):
    clientSockets.append({'socket':socket,'clientName':clientName})
    #print("Inside handleClient Thread")
    #chatLogsTextBox.insert(END, "\n Inside handleClient Thread")
    while True:
        try:
            message = socket.recv(1024).decode('utf-8')
            #print("Server got "+message)
            chatLogsTextBox.insert(END, "\n"+clientName+":"+message)
            if message.startswith("@private"):
                broadCast(clientName + ":" + message,True)
            else:
                broadCast(clientName+":"+message,False)
        except ConnectionResetError:
            socket.close()
            clientSockets.remove({'socket':socket,'clientName':clientName})
            broadCast("-------------------------"+clientName+" left the chat-------------------------")
            #print(clientName,"closed connection")
            chatLogsTextBox.insert(END, "\n"+clientName+" closed connection")
            break
        except ConnectionAbortedError as e:
            socket.close()
            clientSockets.remove({'socket':socket,'clientName':clientName})
            broadCast("-------------------------" + clientName + " left the chat-------------------------")
            # print(clientName,"closed connection")
            chatLogsTextBox.insert(END, "\n" + clientName + " closed connection")
            break
        except ConnectionError as e:
            socket.close()
            clientSockets.remove({'socket':socket,'clientName':clientName})
            broadCast("-------------------------" + clientName + " left the chat-------------------------")
            # print(clientName,"closed connection")
            chatLogsTextBox.insert(END, "\n" + clientName + " closed connection")
            break


def main():
    while True:
        c,addr = socketObj.accept()
        #print('connected to:'+addr[0]+':'+str(addr[1]))
        chatLogsTextBox.insert(END, "\n connected to:"+addr[0]+":"+str(addr[1]))
        addresses.append(addr)
        data = str(c.recv(1024).decode("UTF-8")).split(":")
        clientName = str(data[0]).lower()
        password = str(data[1])
        clientNames.append(str(clientName).lower())
        #print("Clients Present",clientNames)
        chatLogsTextBox.insert(END, "\n Clients Present"+str(clientNames))

        #check the number of users having same name
        usernameUsageCount = 0
        usernameInLowerCase = str(clientName).lower()
        for i in range(0,len(clientNames)):
            if usernameInLowerCase==clientNames[i]:
                usernameUsageCount+=1
        if usernameUsageCount>1:
            #print("Username usage count = ",usernameUsageCount)
            #chatLogsTextBox.insert(END, "\n Username usage count = " + str(usernameUsageCount))
            c.send("UsernameAlreadyUsed".encode("UTF-8"))
            clientNames.remove(str(clientName).lower())
            c.close()
        elif password!=serverPassword:
            c.send("IncorrectPassword".encode("UTF-8"))
            clientNames.remove(str(clientName).lower())
            c.close()
        else:
            c.send("EverythingIsFine".encode("UTF-8"))
            #message = "Welcome "+str(clientName)+" "
            #print(message)
            chatLogsTextBox.insert(END, "\n "+clientName+" joined the chat")
            broadCast("-----------------------" + clientName + " joined the chat-----------------------")
            '''c.send(message.encode("UTF-8"))
            print(c.recv(1024).decode('utf-8'))'''
            threading.Thread(target=handleClient,args=(c,clientName,)).start()


threading.Thread(target=main).start()
window.mainloop()