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
        q.put(self.data) #test for the queue, later the prepare func will put() in the queue
        ff.writter(q)

if __name__ == "__main__":
    q = queue.Queue() #AGREGAR PRIORIDADES

    #thread for starting the writter, now it's started by the handler, it won't in a while
    #t1 = threading.Thread(target= writter,args=(q,))
    
    address = ("192.168.1.51", 8080) #host ip, port)
    servidor = TcpThreads(address,ServerHandler) #uses the TcpThread class then handler class
    servidor.allow_reuse_address = True #reuse address when the server is restarted
    servidor.serve_forever() #continue handling request until ctrl+c passed
