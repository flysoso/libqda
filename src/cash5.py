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


a=0
b=0
c=0
d=0

iu = 0
for i in dayline:
    if iu:
        if i.op > iu.cl:
            if i.cl > i.op:
                a+=1
            else:
                b+=1
        else:
            if i.cl > i.op:
                c+=1
            else:
                d+=1
    iu = i

print a,b,c,d

print a+d, b+c
#test sub_area
#print sub_area([[1,4],[2,8],[4,32]])