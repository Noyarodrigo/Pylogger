#aathis submodule contains the reader/writter/prepare functions for main.py (server)
from datetime import datetime
import multiprocessing
import re


manager = multiprocessing.Manager() 
temperature = manager.list() #manager is for global shared list (or other objects) between processes
temperature = [0]*3 #here would be the number of sensor you are using, it'd be taken from a config file
count = manager.Value('i',0)
humidity = manager.list() 
humidity = [0]*3

def writer(q,qa,lk_file):
    buff = [] #this would be a buffer to save a certain amounts of lectures until you open the file and write, it's a performance test
    read = []
    limit = 35 #this limit should be taken from the conf file
    while True:
        if not q.empty():
            read = q.get()
            if float(read[1]) >= limit: #alarm
                qa.put(read)
            buff.append(read)
            if len(buff) >= 10: #block and wrtie the file
                lk_file.acquire()
                with open ('lectures.csv', 'a') as lectures:
                    print('-.-.-writing in file-.-.-')
                    for el in buff:
                       lectures.write(str(el)+'\n')
                lk_file.release()
                buff = []

def prepare(data,q):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    splited = str(data).split('/')
    splited = [i.strip('THID=') for i in splited]
    splited = splited[1:4]
    splited.append(timestamp)
    q.put(splited)
   
def average():
    avg_temperature = []
    avg_humidity = []
    for i in range(len(temperature)):
        avg_temperature.append(round(temperature[i]/count.value,2))
        avg_humidity.append(round(humidity[i]/count.value,2))

    print('--------------------------------------')
    print('Average Temp:{}\nAverage Hum:{}\n--------------------------------------'.format(avg_temperature,avg_humidity))
    
    return avg_temperature,avg_humidity;

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
    
    print('--------------------------------------')
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
    

