import socketserver
import queue as queue
import threading
import file_funcs as ff
import multiprocessing


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

    q = multiprocessing.Queue() #AGREGAR PRIORIDADES
    lk = multiprocessing.Lock() #file concurrency

    try:
        w = multiprocessing.Process(target=ff.writter,  args=(q,))
        w.start()
        print('Writter Process ... OK')
    except:
        print('Writter Process ... Failed')
        print('-Warning, no records will be held from this point-')

    address = ("192.168.1.51", 8080) #host ip, port)
    servidor = TcpThreads(address,ServerHandler) #uses the TcpThread class then handler class
    
    #continue handling request until ctrl+c passed
    try:
        print('Server Process ... OK')
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.shutdown()
        servidor.socket.close()
