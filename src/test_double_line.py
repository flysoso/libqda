execfile("E:\\dev\\dev_eclipse\\libqda\\src\\_reg.py")

import libqda
import wx_show_graph_2
import math
import pickle_util
import sys

# simple show graph

print sys.argv

libqda.qda_init()
arr_list = libqda.get_all_index_arr( filter = 1)
p = arr_list[0]
print p.fname
dayline = libqda.get_line_arr_fdaydata(p)


def tp1graph():

	'''
		
		THIS SORT OF PROGRAM 
		GAVE T+1 GRAPH

	'''

	# init val make no bug
	pre_op = dayline[0].op
	graph_list = ['line']
	
	graph2_list = ['line']
	
	itt = 0

	# circle calculation
	
	print ' ------------------ '
	
	for k in dayline:
		itt += 1
		if 0:
			newItem = [itt, k.op - pre_cl]
			pre_cl = k.cl
		if 1:
			newItem = [itt, k.op - pre_op]
			pre_op = k.op
		graph_list.append( newItem )
		graph2_list.append( [itt, math.cos(itt / 100.0) * 1])
		

	wx_show_graph_2.show_graph(		[graph_list, graph2_list]	)

tp1graph()

#test sub_area
#print sub_area([[1,4],[2,8],[4,32]])