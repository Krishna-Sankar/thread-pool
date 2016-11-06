import socket
from threading import Thread

class Client(Thread):
    def __init__(self):
        Thread.__init__(self) 

    def run(self):
        while True:
            data = conn.recv(2048)
            print "Server received data:", data
            conn.send("pong")

PORT = 3000 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind(("0.0.0.0", PORT))
pool = [] 

while True:
    # At most one queued client
    server.listen(1)
    (conn, (ip,port)) = server.accept() 
    clientThread = Client()
    clientThread.start()
    pool.append(clientThread)

# Wait for every thread to finish
for thread in pool:
    thread.join()