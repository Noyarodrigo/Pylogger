import socketserver
import queue as queue
import threading
import file_funcs as ff

class TcpThreads(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ServerHandler(socketserver.BaseRequestHandler):
    def setup(self):
        print("New connection from: ",self.client_address[0])
    def handle(self):
        self.data = self.request.recv(1024)
        #here would be the parse/strip/prepare func for putting in the queue the sensor read for the writter to take (get())
        ff.prepare(self.data,q)

if __name__ == "__main__":
    q = queue.Queue() #AGREGAR PRIORIDADES

    #thread for starting the writter
    t1 = threading.Thread(target= ff.writter,args=(q,))
    t1.daemon = True
    t1.start()

    address = ("192.168.1.51", 8080) #host ip, port)
    servidor = TcpThreads(address,ServerHandler) #uses the TcpThread class then handler class
    servidor.allow_reuse_address = True #reuse address when the server is restarted
    servidor.serve_forever() #continue handling request until ctrl+c passed
