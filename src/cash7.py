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

def get_trough_id(dayline, bound = 5):
    result = []
    for i in range(bound, len(dayline) - bound):
        skipthis = 0
        for k in range(-bound,0):
            if dayline[i+k].op < dayline[i].op:
                skipthis = 1
                break
        if skipthis: continue
        for k in range(1, bound+1):
            if dayline[i+k].op < dayline[i].op:
                skipthis = 1
                break
        if skipthis: continue
        #print 'this is a trough'
        thistrough = i
        #for k in range(i-bound, i+bound):
        #    print k, dayline[k].op
        #print '------', i
        result.append(thistrough)
    return result    

trough_id = get_trough_id(dayline)

def get_rate(dayline, offset1 = 10, offset2 = 5):
    a = 0
    b = 0
    for i in trough_id:
        if i+offset1 > len(dayline)-1: break
        if dayline[i+offset1].op - dayline[i+offset2].op > 0:
            a+=1
        else:
            b+=1
    return float(a)/(a+b)

print get_rate(dayline, 20, 5)