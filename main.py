import socketserver
import queue as queue
import threading
import file_funcs as ff
from startup import *

class TcpThreads(socketserver.ThreadingMixIn, socketserver.TCPServer):
    socketserver.TCPServer.allow_reuse_address = True #reuse address when the server is restarted
    pass

class ServerHandler(socketserver.BaseRequestHandler):
    def setup(self):
        print("New connection from: ",self.client_address[0])
    def handle(self):
        self.data = self.request.recv(1024)
        #prepare the string to add to the queue
        ff.prepare(self.data,q)

if __name__ == "__main__":

    q = multiprocessing.Queue() 
    qa = multiprocessing.Queue() #queue for the alert process
    lk_file = multiprocessing.Lock() #file concurrency

    startup(q,qa,lk_file)
    servidor = TcpThreads(address,ServerHandler) #uses the TcpThread class then handler class
    run(servidor)

