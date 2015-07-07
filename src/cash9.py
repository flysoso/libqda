import libqda
import wx_show_graph
import math
import pickle_util

libqda.qda_init()
arr_list = libqda.get_all_index_arr( filter = 1)
p = arr_list[222]
print p.fname

dayline = libqda.get_line_arr_fdaydata(p)
#wx_show_graph.show_graph(dayline) 

arr = [[0 for i in range(23)] for j in range(23)]

u = dayline[0]
pru = u.cl / u.op - 1
if pru > 0.11:  pru = 0.11
if pru < -0.11: pru = -0.11


for i in dayline[1:]:
    
    
    pr1 = i.cl / i.op - 1
    if pr1 > 0.11: pr1 = 0.11
    if pr1 < -0.11: pr1 = -0.11
        
    a = int(pr1*100)+11
    b = int(pru*100)+11
    
    print pr1, pru, a,b
    
    arr[a][b]+=1
    
    pru = pr1
    u = i

for i in arr:
    print i


for i in range(0,23):
    sum = 0
    for j in range(0,23):
        sum += arr[i][j]
    for j in range(0,23):
        print i-11,j-11," __to__ ", arr[i][j]/float(sum)*100
    print

for i in range(0,23):
    sum = 0
    for j in range(0,23):
        sum += arr[j][i]
    for j in range(0,23):
        print i-11,j-11," __from__ ", arr[j][i]/float(sum)*100
    print

# this means percent to percent jilv