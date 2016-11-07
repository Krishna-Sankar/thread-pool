import socket, errno
from threading import Thread

class Client(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            data = self.conn.recv(2048)
            if data != "":
                print "Server received data:", data
            try:
                self.conn.send("pong")
            except IOError as e:
                print "Client unreachable"
                break

PORT = 3000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", PORT))
pool = []

while True:
    # At most one queued client
    server.listen(1)
    (conn, (ip,port)) = server.accept()
    clientThread = Client(conn)
    clientThread.start()
    pool.append(clientThread)

# Wait for every thread to finish
for thread in pool:
    thread.join()