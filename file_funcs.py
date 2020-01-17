#this submodule contains the reader/writter functions for main.py (server)

def writter(q):
    #agregar lock para el lector
    print(q.get())
    #liberar

def reader():
    #lock
    #read
    #release
    pass

def prepare():
    #some work here, it depends on how the string from the esp8266 gonna be
    pass
