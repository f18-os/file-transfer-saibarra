import socket
import threading
import os

def RetrFile(name, sock):
    filename = sock.recv(1024)

    if os.path.isfile(filename):
        sock.send("EXISTS " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "": 
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR")
    sock.close()

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind( (host,port) )
    #socket and bind to port 5000

    s.listen(5)
    #listen with backlog of 5 queued connections

    print "Server started NOW..."
    while True:
        c, addr = s.accept()
        print "client connected ip:<" + str(addr) + ">"
        t = threading.Thread(target = RetrFile, args = ("retrThread", c) )
        t.start()
    s.close()

if __name__ == '__main__':
    Main()
        
