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

def dayline_continuable(dl):
    u = []
    ku = dl[0]
    u.append(ku)
    for k in dl[1:]:
        t1 = k.ftime / 86400
        t2 = ku.ftime / 86400
        for i in range(t2 + 1, t1):
            u.append(-1)
        ku = k
    u.append(k)
    return u

lastsummit = -9999
sumarea = [0 for i in range(0,334)]
chg = 0

def found_a_summit_so_update_frequence(ts):
    global lastsummit
    global sumarea

    if (lastsummit + 9999):
        qu = ts - lastsummit
        if qu < 11:
            return
        #print qu
        if qu > 333: qu = 333
        sumarea[int(qu/2)]+=1
    lastsummit = ts

def get_summit(dayline, bound = 5):
    result = []
    for i in range(bound, len(dayline) - bound):
        skipthis = 0
        for k in range(-bound,0):
            if dayline[i+k].op > dayline[i].op:
                skipthis = 1
                break
        if skipthis: continue
        for k in range(1, bound+1):
            if dayline[i+k].op > dayline[i].op:
                skipthis = 1
                break
        if skipthis: continue
        #print 'this is a summit'
        thissummit=dayline[i].time2000()
        #for k in range(i-bound, i+bound):
        #    print k, dayline[k].op
        #print '------', i
        result.append(thissummit)
    return result

au = get_summit(dayline,bound = 100)
print au

dayline = libqda.get_line_arr(p)

wx_show_graph.set_sign_x( au )
wx_show_graph.show_graph( dayline )


'''

BELOW should be put into another cashXX I think

for i in au:
    found_a_summit_so_update_frequence(i)
    
# sumarea[i]:  length between two summit appear frequency, every col divided by 2 default
a = []
xx = []
for i in range(1, len(sumarea)):
    xx.append([i, sumarea[i]])

wx_show_graph.show_graph(xx)
'''