from profiler import profile
import pandas as pd
import inspect
import os
path = os.getcwd()
from datetime import datetime
def comp(inp,module = None):
    """Pass the input and the module whose functions need to be compared. Will return the comparative study."""
    
    li = []
    timer = []
    test = dict()
    for i in inspect.getmembers(module):
        for j in i:
            if inspect.isfunction(j):
                test,time = profile(j,inp)
                li.append(test)
                timer.append(time)
                print("\n\n")
                
    sol = pd.DataFrame(li) 

    df = sol.sort_values(by = ['Execution Time','Cpu Usage','write_bytes','memory_usage','RAM','Number of active threads','read_bytes'], ascending = True)
    print(df[['Function Name','Execution Time','memory_usage','Cpu Usage','write_bytes','read_bytes']])
    minif = df[['Function Name','Execution Time','memory_usage','Cpu Usage','write_bytes','read_bytes']]
    #print(path+'\\Comp\\'+str(module.__name__)+'.csv')
    if os.path.isdir(path):
        pass
    else:
        os.makedirs(path)

    
    
    with open(path+'\\Comp\\'+str(module.__name__)+'.csv','a+') as f1:
        f1.write("\n******************************{}******************************\n".format(datetime.now()))
    
    df.to_csv(path+'\\Comp\\'+str(module.__name__)+'.csv',index = False,mode = 'a+')
    
    with open(path+'\\Comp\\'+str(module.__name__)+'.csv','a+') as f1:
        f1.write("\n******************************END******************************\n")
    
    
    
    with open(path+'\\Comp\\'+str(module.__name__)+'_min.csv','a+') as f1:
        f1.write("\n******************************{}******************************\n".format(datetime.now()))
    
    minif.to_csv(path+'\\Comp\\'+str(module.__name__)+'_min.csv',index = False,mode = 'a+')
    
    with open(path+'\\Comp\\'+str(module.__name__)+'_min.csv','a+') as f1:
        f1.write("\n******************************END******************************\n")