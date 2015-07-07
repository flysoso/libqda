# -*- coding: cp936 -*-

import libqda
from dayline_util import *

''' 这个需要计算一段时间。。。。
    this might need some time to do ...
'''

if __name__ == '__main__':
    libqda.qda_init()
    arr_list = libqda.get_all_index_arr( filter = 1)
    result_list = [];
    for p in arr_list:
        dayline = libqda.get_line_arr(p)
    
        if dayline[-1][0] > 3650:
            sf1 = calculate_factor(dayline[-31:-1])
            sf2 = calculate_factor(dayline[-15:-1])
            sf3 = calculate_factor(dayline[-5:-1])
            sf4 = calculate_minus(dayline[-31:-1])
            sf5 = calculate_minus(dayline[-15:-1])
            sf6 = calculate_minus(dayline[-5:-1])
            sf7 = dayline[-1][1]
        result_list.append([p.fid, sf1, sf2, sf3, sf4, sf5, sf6, sf7])
        
        print p.fname + '\t' + str(sf1)
