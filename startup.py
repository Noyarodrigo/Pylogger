#settings for the server when it starts
import multiprocessing
import file_funcs as ff
import alert as al
import os

address = ("192.168.1.51",8080) #(ip, port)

def startup(q,qa,lk_file):
    if not os.path.exists('lectures.csv'): #check if the file exists and create if it doesn't  
        os.mknod('lectures.csv')
    try:
        ff.reader_full(lk_file) #read the lectures and prepare for averages
        ff.average()
        w = multiprocessing.Process(target=ff.writer,  args=(q,qa,lk_file,)) #cretes and start writter process
        alert = multiprocessing.Process(target=al.sendmail, args=(qa,)) #creates and start the alert process
        w.start()
        alert.start()
        print('Writter Process ... OK')
        print('Alert Process ... OK')

    except:
        print('Writter Process ... Failed')
        print('-Warning, no records will be held from this point-')

def run(servidor):
    try:
        print('Server Process ... OK')
        servidor.serve_forever() #serve until ctrl+c (or other) is passed
    except KeyboardInterrupt:
        servidor.shutdown()
        servidor.socket.close()

