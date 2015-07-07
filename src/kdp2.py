# -*- coding: cp936 -*-

import libqda
import wx_show_graph
import math
import random
import pickle_util

from dayline_util import *


def dissolve_list(mlist):
	rlist = []
	for k in mlist:
		if type(k) is list:
			rlist = rlist + dissolve_list(k)
		else:
			rlist.append(k)
	return rlist
	
def write_result_list_to_file():
	global result_list
	f = open('Z:\\provide2.txt', 'w')
	for k in result_list:
		klist = dissolve_list(k)
		for k1 in klist:
			f.write( str(k1) )
			f.write(' ')
		f.write('\n')
	print "Write to File Finished"

libqda.qda_init()
arr_list = libqda.get_all_index_arr( filter = 1)

result_list = [];

# length for each piece of dayline data, 15 for train, 2 to predict
ppd = 17

# how many lines of data to pick up
rdc = 1000

for k1 in range(0, rdc):
	
	print k1
	
	# random get a stock dataset
	p = arr_list[ int(len(arr_list) * random.random()) ]
	
	# get the dayline data
	dayline = libqda.get_line_arr(p)
	
	# time judgement
	# find the point to begin
	for i in range(len(dayline) - 1, 0, -1):
		if dayline[i][0] < 4000:
			break

	# make sure that range is ok
	range_min = i+1
	range_max = len(dayline) - 1 - ppd
	
	range_len = range_max - range_min
	
	if range_len < 30:
		continue
	
	# generate a position
	rand_pos = range_min + int((range_max-range_min) * random.random())
	
	# the key is part of output data
	simple_key = [p.fid, rand_pos]
	
	# trim the dayline, length = ppd
	dayline = dayline[rand_pos: rand_pos + ppd]
# dayline[2:6]	4 days for train, d1 = 4
# dayline[6:8]	2 days to predict, d2 = 2
# 				length = 8, d3 = 8, last index dayline[7]
	loop_result_list = [simple_key]

	d3 = len(dayline) #length (=ppd)
	d2 = 2	# days to predict
	ddi = [3, 5, 15]
	for i in range(0,3):
		d1 = ddi[i]	# days for train
		
		# data arrangement
		line1 = dayline[d3-d2-d1: d3-d2]
		#line2 = dayline[d3-d2: d3]
	
		loop_result_list.append(	calculate_minus(line1)	)
	for i in range(0,3):
		d1 = ddi[i]
		line1 = dayline[d3-d2-d1: d3-d2]
		loop_result_list.append(	calculate_factor(line1)	)
	
	# var to predict
	c1 = dayline[d3-1][1]
	c2 = dayline[d3-1-d2][1]

	ratio = (c1-c2) / c2	# to be predicted
	
	loop_result_list.append(ratio)

	result_list.append(loop_result_list)

write_result_list_to_file()

