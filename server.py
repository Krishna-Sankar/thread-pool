import socket, time, threading, signal
from threading import Thread

NB_THREADS = 5
PORT = 3000

class Pool():
    def __init__(self):
        self.lockBusy = threading.Lock()
        self.lockClients = threading.Lock()
        self.clients = []
        self.workers = []
        self.busy = 0
        self.killRequested = False
        for counter in range(NB_THREADS):
            self.workers.append(Worker(self, counter))
            self.workers[counter].start()

    def assignClient(self, conn):
        print "Pool has been asked to append a client to the task list"
        self.lockClients.acquire()
        self.clients.append(conn)
        self.lockClients.release()

    def kill(self):
        self.killRequested = True

class Server(Thread):
    def __init__(self, pool):
        Thread.__init__(self)
        self.daemon = True # This thread may die while waiting for a client
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", PORT))
        self.pool = pool

    def run(self):
        while True:
            # At most 4 queued clients
            self.server.listen(4)
            (conn, (ip,port)) = self.server.accept()
            print "Server received client connection"
            self.pool.assignClient(conn)

class Worker(Thread):
    def __init__(self, pool, id):
        Thread.__init__(self)
        self.pool = pool
        self.conn = None
        self.id = id

    def constructReply(self, data):
        reply = "HELO {0}\nIP:{1}\nPort:{2}\nStudentID:{3}\n".format(data, socket.gethostbyname(socket.gethostname()), PORT, 16336617)
        return reply

    def run(self):
        while not self.pool.killRequested:
            # Try to get a client
            self.pool.lockClients.acquire()
            if len(self.pool.clients) > 0:
                self.conn = self.pool.clients.pop(0)
            self.pool.lockClients.release()

            # If we didn't get a client, try again
            if self.conn is None:
                continue

            print "Thread {0} fetched a client".format(self.id)
            # If we have a client, indicate pool that we're busy
            self.pool.lockBusy.acquire()
            self.pool.busy += 1
            self.pool.lockBusy.release()

            # Serve client
            data = self.conn.recv(2048)
            print "Thread {0} received data {1}".format(self.id, data)
            if data == "KILL_SERVICE\n":
                self.pool.kill()
            elif data.startswith("HELO "):
                try:
                    self.conn.send(self.constructReply(data[5:].rstrip()))
                except IOError as e:
                    # Client unreachable, nothing to be done
                    pass

            self.conn.close()
            self.conn = None

            # Indicate pool that we're done
            self.pool.lockBusy.acquire()
            self.pool.busy -= 1
            self.pool.lockBusy.release()
        print "Thread {0} dying".format(self.id)

print "--- Preparing thread pool..."
workerPool = Pool()

print "--- Creating CTRL-C signal handler..."
def signalHandler(signal, frame):
    print "Server received CTRL-C"
    workerPool.kill()
signal.signal(signal.SIGINT, signalHandler)

print "--- TCP server starting..."
serverThread = Server(workerPool)
serverThread.start()
print "--- Server is ready!"

while True:
    if workerPool.killRequested:
        for worker in workerPool.workers:
            worker.join()
        break