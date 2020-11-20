import socket

TCP_IP = '10.0.2.15'
TCP_PORT = 9001
BUFFER_SIZE = 1024

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    choice = str(input("Options (enter corresponding number): \n0. Quit\n1. Request file from server\n2. Request file transfer statistics\n"))

    if choice == '0':
        #send choice to server
        s.send(choice.encode())
        #receive response from server
        message = s.recv(1)
        message = message.decode()
        if message == 'Y':
            print("Server has receiced choice")
        s.close()
        break
    elif choice == '1':
        filename = input("Enter filename : ")
        #send choice to server
        s.send(choice.encode())
        #receive response from server
        message = s.recv(1)
        message = message.decode()
        if message == 'Y':
            print("Server has receiced choice")
        #send filename to server
        s.send(filename.encode())
        #receive response from server
        message = s.recv(1)
        message = message.decode()
        if message == 'Y':
            print("Server has receiced filename")
        #does the file exist?
        message = s.recv(1)
        message = message.decode()
        
        if message == "Y":
            print("File exists")
            receivedfile = filename + "_received"
            with open(receivedfile, 'wb') as f:
                print('File opened')
                while True:
                    #print('receiving data...')
                    data = s.recv(BUFFER_SIZE)
                    print('data=%s', (data))
                    if not data:
                        f.close()
                        print('File closed')
                        break
                    # write data to a file
                    f.write(data)

            print('Successfully transferred the file')
            s.close()

        else:
            print("Error : file does not exist")
            s.close()
            continue
    elif choice == '2':
        #send choice to server
        s.send(choice.encode())
        #receive response from server
        message = s.recv(1)
        message = message.decode()
        if message == 'Y':
            print("Server has receiced choice")

        message = s.recv(1)
        message = message.decode()

        if message == 'Y':
            message = s.recv(BUFFER_SIZE)
            message = message.decode()
            print(message)
        elif message == 'N':
            print("No file transfer history found")
            s.close()
       
print('connection closed')