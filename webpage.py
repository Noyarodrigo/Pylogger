#generates the html with the values
import file_funcs as ff
import matplotlib.pyplot as plt
import numpy as np
import os
import time

def generate_interface(self):
    print('Generating interface for{}'.format(self.client_address))
    self.request.sendall(str.encode("HTTP/1.1 200 OK\n",'iso-8859-1'))
    self.request.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
    self.request.send(str.encode('\r\n'))
    with open ('index.html','r') as index:
        for l in index:
            self.request.sendall(str.encode(""+l+"", 'iso-8859-1'))

def showplot(self,sensor_id,event_id):
    temp,hum = ff.realtime(sensor_id)

    if event_id.is_set():
        event_id.clear()
        plot(temp,hum,sensor_id)
        event_id.set()
    event_id.wait()

    name = 'plots/sensor'+str(sensor_id)+'.png'

    with open(name, 'rb') as f1:
        data = f1.read()
        HTTP_RESPONSE = b'\r\n'.join([
        b"HTTP/1.1 200 OK",
        b"Connection: close",
        b"Content-Type: image/jpg",
        bytes("Content-Length: %s" % len(data) ,'utf-8'),
        b'', data 
        ] )
        self.request.sendall(HTTP_RESPONSE)

def plot(temp,hum,i):

    print(f'Ploteando: id:{i} temp:{temp} hum:{hum}')

    name = 'plots/sensor'+str(i)+'.png'
    if os.path.exists(name): #check if the file exists and delete it  
         os.remove(name)
    fig, ax = plt.subplots()
    x_var = ['Temperature','Humidity']
    plt.xlabel('Variable')
    plt.ylabel('C° , hum%')
    height = [temp,hum]
    y_pos = [0,1] 
    plt.bar(y_pos, height, width=0.4)
    plt.xticks(y_pos, x_var)
    plt.savefig(name)
    plt.cla()
    plt.close(fig)
