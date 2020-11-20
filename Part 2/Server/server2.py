import socket
from threading import Thread
from socketserver import ThreadingMixIn
import os

TCP_IP = '10.0.2.4'
TCP_PORT = 9001
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print("New thread started for "+ ip + ": " + str(port))

    def run(self):
        #get choice from client
        choice = self.sock.recv(1)
        choice = choice.decode()
        message = "Y"
        self.sock.send(message.encode())

        if choice == '0':
            self.sock.close()
            return "quit"
        elif choice == '1':
            #get filename from client
            filename = self.sock.recv(BUFFER_SIZE)
            filename = filename.decode()
            message = "Y"
            self.sock.send(message.encode())

            #check if filename exists
            try:
                f = open(filename,'rb')
                message = "Y"
                self.sock.send(message.encode())

                while True:
                    l = f.read(BUFFER_SIZE)
                    while (l):
                        self.sock.send(l)
                        #print('Sent ',repr(l))
                        l = f.read(BUFFER_SIZE)
                    if not l:
                        f.close()
                        self.sock.close()
                        break

                #add filename to log
                logfilename = "log_" + self.ip + ".txt"
                f = open(logfilename, "a")
                f.write(filename)
                f.write("\n")
                return "done"

            except FileNotFoundError:
                message = "N"
                self.sock.send(message.encode())
                self.sock.close()
                return "done"

        elif choice == '2':
            #file usage stats
            logfilename = "log_" + self.ip + ".txt"

            try:
                f = open(logfilename, "r")
                message = "Y"
                self.sock.send(message.encode())

                transfer_data = ""
                lines = f.readlines()
                
                for line in lines:
                    l = line.rstrip()
                    file_size = str(os.stat(l).st_size)
                    line_data = l + " : " + file_size + " Bytes\n"
                    transfer_data += line_data

                self.sock.send(transfer_data.encode())
                self.sock.close()
                return "done"

            except FileNotFoundError:
                message = "N"
                self.sock.send(message.encode())
                self.sock.close()
                return "done"
        
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    ret = newthread.run()
    threads.append(newthread)

    if ret == "quit":
        break
