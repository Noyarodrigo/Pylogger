#this submodule contains the reader/writter functions for main.py (server)

def writter(q):
    #agregar lock para el lector
    print('Writter Thread started...')
    while True:
        print(q.get())
    #liberar

def reader():
    #lock
    #read
    #release
    pass

def prepare(data,q):
    split = str(data).split('/')
    q.put(split[1:4]) 
