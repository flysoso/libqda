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
	

libqda.qda_init()
arr_list = libqda.get_all_index_arr( filter = 1)

result_list = [];

# length for each piece of dayline data, 15 for train, 2 to predict
ppd = 17

days_to_predict = 2	# days to predict
sample_for_picks = [3, 5, 15]

# ps. for most of the time, samp(max) + dtpredict = ppd

for k in arr_list:
	if k.fid == 'SH600703':
		p=k
		break

# get the dayline data
dayline = libqda.get_line_arr(p)

rand_pos = 3270

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

	print line1
	loop_result_list.append(	calculate_minus(line1)	)
	print calculate_minus(line1)
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

print loop_result_list

raw_input()
