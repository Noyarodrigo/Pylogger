#this submodule contains the reader/writter/prepare functions for main.py (server)
from datetime import datetime
import multiprocessing
import re


manager = multiprocessing.Manager() 
temperature = manager.list() #manager is for global shared list (or other objects) between processes
temperature = [0]*3 #here would be the number of sensor you are using, it'd be taken from a config file
count = manager.Value('i',0)
humidity = manager.list() 
humidity = [0]*3

def writter(q,lk_file):
    while True:
        if not q.empty():
            lk_file.acquire()
            with open ('lectures.csv', 'a') as lectures:
                lectures.write(str(q.get())+'\n')
                print('writting in file: ',q.get())
            lk_file.release()

def prepare(data,q):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    splited = str(data).split('/')
    splited = [i.strip('THID=') for i in splited]
    splited = splited[1:4]
    splited.append(timestamp)
    q.put(splited)
   
def reader_full(lk_file):
    process_me = []

    lk_file.acquire()
    with open ('lectures.csv', 'r') as lectures:
       for line in lectures:
           process_me.append(line)
    lk_file.release()
    
    pool = multiprocessing.Pool(multiprocessing.cpu_count()*2)
    for element in process_me:
        pool.apply_async(calculate, args=(element,), callback=finish)

    #i'm using pool async because it has a call back function that allows to write just 1 time
    #the var so just a lock-release is requiered, i will be adding the values to the id position
    #in the global list
    pool.close()
    pool.join()
    print('Temperatures:',temperature)
    print('Humidities:',humidity)
    print('Lectures:',count.value)

def calculate(string):
    data_per_line = []
    string = string.split(',')
    index = int(string[0].strip("'['"))
    local_temperature = float(re.sub(r'[\']', '',string[1]).strip("'[']'"))#replace non alfanumeric values with spaces then strip them
    local_humidity = float(re.sub(r'[\']', '',string[2]).strip("'[']'"))
    data_per_line.append(index)
    data_per_line.append(local_temperature)
    data_per_line.append(local_humidity)
    return data_per_line

def finish(processed):
    temperature[processed[0]-1] = temperature[processed[0]-1] + processed[1]
    humidity[processed[0]-1] = humidity[processed[0]-1] + processed[2]
    count.value += 1
    

