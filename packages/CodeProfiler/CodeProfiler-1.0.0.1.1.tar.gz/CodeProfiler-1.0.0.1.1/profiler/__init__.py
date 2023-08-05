import threading
import os
import psutil
from timeit import default_timer as timer
import platform
from datetime import datetime
from csv import DictWriter

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
    


def profile(func,param):
    output = dict()
    output['DateTime'] = datetime.now()
    output['Function Name'] = func.__name__
    output["Input"] = param
    start = timer()
    output["Output"]=func(param)
    output["Execution Time"] = timer()-start
    output["Number of active threads"] = threading.active_count()
    output["Machine"] = platform.machine()
    output["Platform Version"] = platform.version()
    output["System"] = platform.system()
    output["Processor"] = platform.processor()
    output['RAM']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    
    py = psutil.Process(os.getpid())
    
    output["Memory Usage"] = py.memory_info()[0]/2.**30
    output["Cpu Usage"] = psutil.cpu_percent()
    output["Virtual Memory"] = psutil.virtual_memory()

    optprinter(output)
    logger(output)



