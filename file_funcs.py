#this submodule contains the reader/writter/prepare functions for main.py (server)

def writter(q):
    #agregar lock para el lector
    while True:
        print('writting in file: ',q.get())
    #liberar

def reader():
    #lock
    #read
    #release
    pass

def prepare(data,q):
    splited = str(data).split('/')
    splited = [i.strip('THID=') for i in splited]
    q.put(splited[1:4])
    
