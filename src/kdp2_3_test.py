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
		if lplist[i+1] == 0:
			print "ERR, average is 0", lplist
			lplist[i+1] = 0.01
		lplist[1+i+n] = lplist[i+n+1] / lplist[i+1]
		lplist[1+i] = lplist[1+i] / dllast
	return lplist

def mod_ratio(rid):
	rtmax = 0.03
	rts = 0.015
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
for k in arr_list:
	if k.fid == 'SH000001':
		print "found"
		dayline = libqda.get_line_arr(k)
		f1 = 4898
		f2 = f1 + 17
		print calculate_minus(dayline[12:15]) / dayline[-1][1]
		break
	
raw_input()

