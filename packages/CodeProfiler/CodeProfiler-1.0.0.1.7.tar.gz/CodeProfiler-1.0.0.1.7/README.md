# profiler
## Repository with code for profiling other functions.

#### Installation command:
pip install CodeProfiler

#### Profiler
Prints the CPU and memory usage.
Logs the output to a log and a csv file too.

~~~python
#Code Sample for python
from bsort import bsort
from profiler import profile

t = [0,10,3,41,2]
profile(bsort,t)


~~~
*Sample output:*

```
DateTime:2020-03-25 11:08:50.311120 \
Function Name:bsort \
Input:[0, 2, 3, 10, 41] \
Output:[0, 2, 3, 10, 41] \
create_time:2020-03-25 11:08:49 \
Execution Time:2.3699999999959864e-05 \
Number of active threads:5 \
Machine:AMD64 \
Platform Version:10.0.18362 \
System:Windows \
Processor:Intel64 Family 6 Model 158 Stepping 9, GenuineIntel \
RAM:8 GB \
Process Priority:32 \
Memory Usage:0.031497955322265625 \
Cores:4 \
Cpu Usage:100.0 \
Virtual Memory:svmem(total=8459030528, available=3618177024, percent=57.2, used=4840853504, free=3618177024) \
memory_usage:0 \
read_bytes:4313098 \
write_bytes:2874 \
no. of threads:9 \
username:LEGION\Shreyas \
LOG path: e:\Git\CodeLibrary\Shreyas\Python\log\ \
CSV path: e:\Git\CodeLibrary\Shreyas\Python\csv\ 
```

#### Comparer
Compares the functions inside a module

Writes the Complete comparison to a file by the name *module_name.csv* in the a child directory by the name comp.
Also writes a minified output of the same to a file by the name *module_name_min.csv* .
~~~python
#Code Sample for python
from profiler import Comparer 
import Sorting
Comparer.comp([54,26,93,17,77,31,44,55,20],Sorting)

~~~

*Sample output:*
```
Function Name:BubbleSort
Input:[17, 20, 26, 31, 44, 54, 55, 77, 93]
Output:[17, 20, 26, 31, 44, 54, 55, 77, 93]
Execution Time:26000
create_time:2020-03-30 13:01:23
DateTime:2020-03-30 13:01:24.587903
Number of active threads:5
Machine:AMD64
Platform Version:10.0.18362
System:Windows
Processor:Intel64 Family 6 Model 158 Stepping 9, GenuineIntel
RAM:8 GB
Process Priority:32
Memory Usage:0.0633392333984375
Cores:4
Cpu Usage:37.6
Virtual Memory:svmem(total=8459030528, available=2446028800, percent=71.1, used=6013001728, free=2446028800)
memory_usage:0
read_bytes:10824458
write_bytes:0
no. of threads:12
username:LEGION\Shreyas
LOG path: e:\Git\CodeLibrary\Shreyas\Python\log\
CSV path: e:\Git\CodeLibrary\Shreyas\Python\csv\



Function Name:InsertionSort
Input:[17, 20, 26, 31, 44, 54, 55, 77, 93]
Output:[17, 20, 26, 31, 44, 54, 55, 77, 93]
Execution Time:24400
create_time:2020-03-30 13:01:23
DateTime:2020-03-30 13:01:24.622781
Number of active threads:5
Machine:AMD64
Platform Version:10.0.18362
System:Windows
Processor:Intel64 Family 6 Model 158 Stepping 9, GenuineIntel
RAM:8 GB
Process Priority:32
Memory Usage:0.06380844116210938
Cores:4
Cpu Usage:33.3
Virtual Memory:svmem(total=8459030528, available=2444365824, percent=71.1, used=6014664704, free=2444365824)
memory_usage:0
read_bytes:10824458
write_bytes:1196
no. of threads:12
username:LEGION\Shreyas
LOG path: e:\Git\CodeLibrary\Shreyas\Python\log\
CSV path: e:\Git\CodeLibrary\Shreyas\Python\csv\



Function Name:MergeSort
Input:[17, 20, 26, 31, 44, 54, 55, 77, 93]
Output:[17, 20, 26, 31, 44, 54, 55, 77, 93]
Execution Time:121400
create_time:2020-03-30 13:01:23
DateTime:2020-03-30 13:01:24.655694
Number of active threads:5
Machine:AMD64
Platform Version:10.0.18362
System:Windows
Processor:Intel64 Family 6 Model 158 Stepping 9, GenuineIntel
RAM:8 GB
Process Priority:32
Memory Usage:0.06406402587890625
Cores:4
Cpu Usage:37.5
Virtual Memory:svmem(total=8459030528, available=2444148736, percent=71.1, used=6014881792, free=2444148736)
memory_usage:0
read_bytes:10824458
write_bytes:2403
no. of threads:12
username:LEGION\Shreyas
LOG path: e:\Git\CodeLibrary\Shreyas\Python\log\
CSV path: e:\Git\CodeLibrary\Shreyas\Python\csv\



Function Name:SelectionSort
Input:[17, 20, 26, 31, 44, 54, 55, 77, 93]
Output:[17, 20, 26, 31, 44, 54, 55, 77, 93]
Execution Time:55300
create_time:2020-03-30 13:01:23
DateTime:2020-03-30 13:01:24.689604
Number of active threads:5
Machine:AMD64
Platform Version:10.0.18362
System:Windows
Processor:Intel64 Family 6 Model 158 Stepping 9, GenuineIntel
RAM:8 GB
Process Priority:32
Memory Usage:0.06406784057617188
Cores:4
Cpu Usage:87.5
Virtual Memory:svmem(total=8459030528, available=2444124160, percent=71.1, used=6014906368, free=2444124160)
memory_usage:0
read_bytes:10824458
write_bytes:3608
no. of threads:12
username:LEGION\Shreyas
LOG path: e:\Git\CodeLibrary\Shreyas\Python\log\
CSV path: e:\Git\CodeLibrary\Shreyas\Python\csv\



   Function Name  Execution Time  memory_usage  Cpu Usage  write_bytes  read_bytes
1  InsertionSort           24400             0       33.3         1196    10824458
0     BubbleSort           26000             0       37.6            0    10824458
3  SelectionSort           55300             0       87.5         3608    10824458
2      MergeSort          121400             0       37.5         2403    10824458
```