
import socketserver
import Queue
import threading

class TcpThreads(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ServerHandler(socketserver.BaseRequestHandler):
    def setup(self):
        print("New connection from: ",self.client_address[0])
    def handle(self):
        self.data = self.request.recv(1024)
        q.put()
        pass

def writter():
    #agregar lock para el lector
    q.get()
    #liberar

if __name__ == "__main__":
    q = Queue.Queue() #AGREGAR PRIORIDADES
    t1 = threading.Thread(target= writter,args=(q,))
    address = ("192.168.1.51", 8080) #localhost could be changed to an static ip
    servidor = TcpThreads(address,ServerHandler) #uses the TcpThread class then handler class
    servidor.allow_reuse_address = True #reuse address when the server is restarted
    servidor.serve_forever() #continue handling request until ctrl+c passed
