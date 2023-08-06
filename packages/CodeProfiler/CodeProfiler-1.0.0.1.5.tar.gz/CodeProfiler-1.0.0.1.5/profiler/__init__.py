import threading
import os
import psutil
from timeit import default_timer as timer
import platform
from datetime import datetime
from csv import DictWriter
from copy import deepcopy
def optprinter(output):
    for i in output.keys():
        print('{}:{}'.format(i,output[i]))

def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    dict_of_elem.pop('Function Name')
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)



def logger(output):
    lpath = os.getcwd()+'\\log\\'
    cpath = os.getcwd()+'\\csv\\'
    print("LOG path:",lpath)
    print("CSV path:",cpath)

    dirCreate(lpath)
    dirCreate(cpath)

    with open(lpath+str(output['Function Name'])+'.log','a+') as f1:
        f1.write('\n********************************{}********************************\n'.format(output['DateTime']))
        for i in output.keys():
            f1.write('{}:{}\n'.format(i,output[i]))
        f1.write('\n********************************Log End********************************\n')
    
    append_dict_as_row(cpath+str(output['Function Name'])+'.csv',output,output.keys())

    

    
def dirCreate(path):
    if os.path.isdir(path):
        pass
    else:
        os.makedirs(path)
    


def profile(func,param=None):
    output = dict()
    py = psutil.Process(os.getpid())
    
    output["Input"] = param
    start = timer()
    output["Output"]=func(param)
    try:
        output["create_time"] = datetime.fromtimestamp(py.create_time())
    except OSError:
        output["create_time"] = datetime.fromtimestamp(psutil.boot_time())
    output['DateTime'] = datetime.now()
    output['Function Name'] = func.__name__
    output["Execution Time"] = timer()-start
    output["Number of active threads"] = threading.active_count()
    output["Machine"] = platform.machine()
    output["Platform Version"] = platform.version()
    output["System"] = platform.system()
    output["Processor"] = platform.processor()
    output['RAM']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    
    
    output["Process Priority"] = int(py.nice())
    output["Memory Usage"] = py.memory_info()[0]/2.**30
    output["Cores"] = psutil.cpu_count()
    output["Cpu Usage"] = psutil.cpu_percent()
    output["Virtual Memory"] = psutil.virtual_memory()
    try:
        output["memory_usage"] = py.memory_full_info().uss
    except psutil.AccessDenied:
        output["memory_usage"] = 0

    io_counters = py.io_counters()
    output["read_bytes"] = io_counters.read_bytes
    output["write_bytes"] = io_counters.write_bytes
    output["no. of threads"] = py.num_threads()


    try:
        output["username"] = py.username()
    except psutil.AccessDenied:
        output["username"] = "N/A"

    cpy = deepcopy(output)
    optprinter(cpy)
    logger(cpy)

    return output

