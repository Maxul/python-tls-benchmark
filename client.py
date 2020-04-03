import socket, ssl
import threading
import time
from timeit import default_timer as timer

HOST, PORT = '127.0.0.1', 1234

def handle(conn):
    conn.write(b'GET / HTTP/1.1\n')
    # print(conn.recv().decode())
    conn.recv().decode()

def https_client(port):
    sock = socket.socket(socket.AF_INET)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile="client.crt", keyfile="client.key")
    context.load_verify_locations("root.pem")
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
    ssl.match_hostname = lambda cert, hostname: hostname == cert['subjectAltName'][0][1]
    conn = context.wrap_socket(sock, server_hostname=HOST)
    try:
        conn.connect((HOST, port))
        handle(conn)
    finally:
        conn.close()

class myThread (threading.Thread):
    def __init__(self, threadID, name, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.port = port
    def run(self):
        https_client(self.port)

if __name__ == '__main__':
    threads = []
    tic = timer()
    
    for x in xrange(1,10):
        thread = myThread(x, "HTTPS-SERVER", 9000 + x)
        thread.start()
        threads.append(thread)
    
    for t in threads:
        t.join()

    toc = timer()
    print(toc - tic)
