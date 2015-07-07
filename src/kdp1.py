# -*- coding: cp936 -*-

import libqda
import wx_show_graph
import math
import random
import pickle_util

from dayline_util import *


def write_result_list_to_file():
    global result_list
    f = open('Z:\\dataset.txt', 'w')
    for r1 in result_list:
        f.write( r1[0][0] )
        f.write( ' ' )
        f.write( str(r1[0][1]) )
        f.write( ' ' )
        for k in range(1,8):
            f.write( str(  r1[k]  ) )
            f.write(' ')
        f.write( '\n' )
    f.close()
    print "Write to File Finished"

libqda.qda_init()
arr_list = libqda.get_all_index_arr( filter = 1)

result_list = [];

ppd = 30

rdc = 1000

for k1 in range(0, rdc):
    
    print k1
    
    p = arr_list[ int(len(arr_list) * random.random()) ]
    
    dayline = libqda.get_line_arr(p)
    
    ''' 时间约束 > 4000, 数组长度约束 > 30 
    '''
    if dayline[-1][0] < 4000 + ppd:
        continue
    
    for i in range(len(dayline) - 1, 0, -1):
        if dayline[i][0] < 4000:
            break

    range_min = i+1
    range_max = len(dayline) - 1 - ppd
    
    range_len = range_max - range_min
    
    if range_len < 30:
        continue
    
    rand_pos = range_min + int((range_max-range_min) * random.random())
    
    simple_key = [p.fid, rand_pos]
    
    dayline = dayline[rand_pos: rand_pos + ppd]

    sf1 = calculate_factor(dayline[-31:-1])
    sf2 = calculate_factor(dayline[-15:-1])
    sf3 = calculate_factor(dayline[-5:-1])
    sf4 = calculate_minus(dayline[-31:-1])
    sf5 = calculate_minus(dayline[-15:-1])
    sf6 = calculate_minus(dayline[-5:-1])
    sf7 = float(dayline[-1][1] - dayline[-2][1]) / dayline[-2][1]
    
    result_list.append([simple_key, 
                   sf1, sf2, sf3, sf4, sf5, sf6, sf7, dayline])

write_result_list_to_file()

