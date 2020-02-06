import socketserver
import queue as queue
import threading
import file_funcs as ff
from startup import *
import webpage as wp

class TcpThreads(socketserver.ThreadingMixIn, socketserver.TCPServer):
    socketserver.TCPServer.allow_reuse_address = True #reuse address when the server is restarted
    pass

class ServerHandler(socketserver.BaseRequestHandler):
    def setup(self):
        print("New connection from: ",self.client_address[0])
    def handle(self):
        self.data = self.request.recv(1024)
        #detects whether a sensor is connecting or a browser
        if 'User' in str(self.data):
            #if user is present in the request then is a browser, generate and send the html
            #if there is an id in the request plot it and return it, else return the form
            if (str(self.data).find('id=')) != -1:
                wp.showplot(self) 
            else:
                wp.generate_interface(self)
        else:
            #prepare the string to add to the queue
            ff.prepare(self.data,q)

if __name__ == "__main__":

    q = multiprocessing.Queue() 
    qa = multiprocessing.Queue() #queue for the alert process
    lk_file = multiprocessing.Lock() #file concurrency

    startup(q,qa,lk_file)
    servidor = TcpThreads(address,ServerHandler) #uses the TcpThread class then handler class
    run(servidor)

