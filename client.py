import socket 

HOST = socket.gethostname()
PORT = 3000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.connect((HOST, PORT))

while True:
    serverSocket.send("ping")     
    data = serverSocket.recv(2048)
    print "Client received data:", data
    raw_input("Press any key to send other messages...")

serverSocket.close() 