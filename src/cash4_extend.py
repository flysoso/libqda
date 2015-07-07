import libqda
import wx_show_graph
import math
import pickle_util

# simple show graph

libqda.qda_init()
arr_list = libqda.get_all_index_arr( filter = 1)
p = arr_list[0]
print p.fname
dayline = libqda.get_line_arr_fdaydata(p)


dayline = libqda.dayline_plot_data(dayline)
wx_show_graph.show_graph(dayline)



#test sub_area
#print sub_area([[1,4],[2,8],[4,32]])