import socket,threading,random

socketObj = socket.socket()

socketObj.bind(('',10345))

socketObj.listen(6)
addresses = []
clientNames = []
clientSockets = []
serverPassword = str(random.randrange(100000,999999))
print("Password = "+str(serverPassword))
def broadCast(message):
    print("Inside broadcast")
    for client in clientSockets:
        client.send(message.encode("UTF-8"))

def handleClient(socket,clientName):
    clientSockets.append(socket)
    print("Inside handleClient Thread")
    while True:
        try:
            message = socket.recv(1024).decode('utf-8')
            print("Server got "+message)
            broadCast(clientName+":"+message)
        except ConnectionResetError:
            clientSockets.remove(socket)
            broadCast("-------------------------"+clientName+" left the chat-------------------------")
            print(clientName,"closed connection")
            break



while True:
    c,addr = socketObj.accept()
    print('connected to:'+addr[0]+':'+str(addr[1]))
    addresses.append(addr)
    data = str(c.recv(1024).decode("UTF-8")).split(":")
    clientName = str(data[0])
    password = str(data[1])
    clientNames.append(str(clientName).lower())
    print("Clients Present",clientNames)
    #check the number of users having same name
    usernameUsageCount = 0
    usernameInLowerCase = str(clientName).lower()
    for i in range(0,len(clientNames)):
        if usernameInLowerCase==clientNames[i]:
            usernameUsageCount+=1
    if usernameUsageCount>1:
        print("Username usage count = ",usernameUsageCount)
        c.send("UsernameAlreadyUsed".encode("UTF-8"))
        clientNames.remove(str(clientName).lower())
        c.close()
    elif password!=serverPassword:
        c.send("IncorrectPassword".encode("UTF-8"))
        clientNames.remove(str(clientName).lower())
        c.close()
    else:
        c.send("EverythingIsFine".encode("UTF-8"))
        message = "Welcome "+str(clientName)+" "
        print(message)
        '''c.send(message.encode("UTF-8"))
        print(c.recv(1024).decode('utf-8'))'''
        threading.Thread(target=handleClient,args=(c,clientName,)).start()