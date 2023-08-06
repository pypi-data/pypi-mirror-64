
import os
try:
    import psutil
except ImportError as e:
    import pip
    pip.main('install','-q','psutil')
from timeit import default_timer as timer

def profile(func,param):
    print("Input:",param)
    start = timer()
    print("Output:",func(param))
    print("Execution Time:", timer()-start)


    py = psutil.Process(os.getpid())
    memoryUse = py.memory_info()[0]/2.**30
    print("MemoryUsage:",memoryUse,"\ncpuUsage:",psutil.cpu_percent(),"\nVirtualMemory:",psutil.virtual_memory())

