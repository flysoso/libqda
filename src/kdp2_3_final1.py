# -*- coding: cp936 -*-

# SUFFIX OF DAYLINE CARE.

# dayline[2:6]	4 days for train, d1 = 4
# dayline[6:8]	2 days to predict, d2 = 2
# 				length = 8, d3 = 8, last index dayline[7]

import libqda
import wx_show_graph
import math
import random
import pickle_util

from dayline_util import *


def detach_divident(dayline):
	for k in range(1, len(dayline)):
		if (dayline[k-1][1] * (1+0.11) < dayline[k][1]) |	\
			(dayline[k-1][1] * (1-0.11) > dayline[k][1]):
			rrt = float(dayline[k][1]) / dayline[k-1][1]
			for k1 in range(k, len(dayline)):
				dayline[k1][1] = dayline[k1][1] * rrt;
			print "divident_detached", dayline[0]
	return dayline
	
def detach_average( lplist, dllast ):
	n = ( len(lplist) - 2) / 2
	for i in range(1, n+1):
		lplist[i+n] = lplist[i+n] / dllast
		lplist[i] = lplist[i] / dllast
	return lplist

def mod_ratio(rid):
	return rid
	rtmax = 0.015
	rts = 0.05
	if rid > rtmax:
		return 2
	if rid > rts:
		return 1
	if rid > -rts:
		return 0
	if rid > -rtmax:
		return -1
	return -2

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
	f.write('fid time_offset min1 min2 min3 fac1 fac2 fac3 rd \n')
	for k in result_list:
		klist = dissolve_list(k)
		klist[-1] = mod_ratio(klist[-1])
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

days_to_predict = 2	# days to predict
sample_for_picks = [3, 5, 15]

# ps. for most of the time, samp(max) + dtpredict = ppd

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
	
	# detach divident
	dayline = detach_divident(dayline)
	
	# SUFFIX OF DAYLINE CARE.

	loop_result_list = [simple_key]

	d3 = ppd #length (=ppd)
	d2 = days_to_predict	# days to predict
	ddi = sample_for_picks
	
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

	loop_result_list = detach_average(loop_result_list, dayline[-1][1])
	
	result_list.append(loop_result_list)

write_result_list_to_file()

