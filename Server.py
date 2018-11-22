import socket,threading,sys

socketObj = socket.socket()

socketObj.bind(('',10345))

socketObj.listen(6)
addresses = []
clientSockets = []
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
            print(clientName,"closed connection")



while True:
    c,addr = socketObj.accept()
    print('connected to:'+addr[0]+':'+str(addr[1]))
    addresses.append(addr)
    clientName = c.recv(1024).decode("UTF-8")
    message = "Welcome "+str(clientName)+" "
    print(message)
    '''c.send(message.encode("UTF-8"))
    print(c.recv(1024).decode('utf-8'))'''
    threading.Thread(target=handleClient,args=(c,clientName,)).start()