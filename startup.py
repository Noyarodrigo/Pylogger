#settings for the server when it starts
import multiprocessing
import file_funcs as ff
import os

address = ("192.168.1.51", 8080) #host ip, port)

def startup(q,lk):
    if not os.path.exists('lectures.csv'): 
        os.mknod('lectures.csv')
    try:
        w = multiprocessing.Process(target=ff.writter,  args=(q,lk))
        w.start()
        print('Writter Process ... OK')
    except:
        print('Writter Process ... Failed')
        print('-Warning, no records will be held from this point-')

def run(servidor,lk_file):
    try:
        print('Server Process ... OK')
        ff.reader_full(lk_file)
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.shutdown()
        servidor.socket.close()

