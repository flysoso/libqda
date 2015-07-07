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

u = dayline[0]
ku = 0
combo = 0
a=0
b=0
c=0
d=0


for k in range(1,80):
    for i in dayline[1:]:
        if u.cl > u.op:
            if i.op > u.cl * (1+float(k)/100):  #zhang hou gao kai
                a+=1
            else:
                b+=1
        else:
            if i.op > u.cl * (1+float(k)/100):  #die hou gao kai
                c+=1
            else:
                d+=1
        u = i
    print float(a+d)/len(dayline)
    


