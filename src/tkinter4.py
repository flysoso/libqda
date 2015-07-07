# -*- coding: cp936 -*-

from Tkinter import *
import tkMessageBox
import random
import libqda
import time
import cat
import canv_util
import wx_show_graph

#http://blog.csdn.net/jcodeer/article/details/1811310
#Tkinter教程之Listbox篇

class ui_tk:
	def lb1_click(self,event):
			cu = self.lb1.curselection()
			
			# no selection patch
			#----------------
			if len(cu) == 0:
				cur = self.cur
			else:
				cur = int(cu[0])
				self.cur = cur

			# arr = [name,fid,cursor,daycount]

			#print "		attached to index " + str( arr_index [ cur ][ 0 ]) 
			
			target = int(self.arr_index[cur].fcursor)		
			
			print "__________________________________"
			print "60: cursor = " + str(target);
			#print "-------------"
			
			p = libqda.get_by_cursor( target )
			
			#self.cur_data = p
			
			#draw line
			
			time1 = time.time()
			
			self.line_arr = libqda.get_line_arr( p )
			
			#canv_util.canv_draw_stline(self.canv ,arr, restrict_time = self.restrict_time, fixstyle = self.fixstyle)
			wx_show_graph.show_graph(self.line_arr)
			
			arr = None

			print "   60: load time consumed : " + str(time.time() - time1)

	def ui_tell(self, string):
		self.label1["text"] = string
		
	def ui_cat_comm(self, event):
		cat.getcomm( self, self.entry1.get() )
		
	def stat_show(self, stat):
		self.label1["text"] = stat
		
	def gui_create(self):
		
		rt = Tk()
		
		# coordinate the window
		rt.geometry("+200+0") 
				
		lb1 = Listbox(rt, height = 20,width = 22)
		lb1.pack(side = LEFT, fill = "both")
		lb1.bind("<Double-Button-1>", self.lb1_click)
		
		scroll = Scrollbar(rt)
		scroll.pack(side = LEFT, fill = "y")
		
		lb1['yscrollcommand'] = scroll.set
		scroll['command'] = lb1.yview

		canv = Canvas(rt, height=800, width = 1024)
		canv.pack()

		entry1 = Entry(rt, width = 100)
		entry1.pack( )
			
		label1 = Label(rt, anchor = 'w',width = 100)
		label1["text"] = "  This is a status_bar"
		label1.pack(side = LEFT)
		
		btn1 = Button(rt, width = 20, text = "Return")
		btn1.pack( side = LEFT)
		btn1.bind('<1>', self.ui_cat_comm)

		self.lb1 = lb1
		self.canv = canv
		self.scroll = scroll
		self.label1 = label1
		self.entry1 = entry1
		self.rt = rt
		
	def init_tkgui(self):
		
		self.gui_create()
	
		self.gain_arr()
		
		self.restrict_time = []
		self.fixstyle = 0
		
		#self.ui_cat_comm("f,5")
		
		self.rt.mainloop()
	
	def gain_arr(self):
		libqda.qda_init() 
		
		#  -- get all_list --
		arr_index = libqda.get_all_index_arr(filter = 1)
		
		#print arr_index;
		
		#  -- get list from file
		#arr_index = libqda.get_index_from_file("list1.lst")
		
		# -- filter
		# the format is [p.fname,p.fid, p.fcursor, p.daycount]
		
		for i in range(0, len(arr_index)):
			self.lb1.insert(END, arr_index[i].fname.decode('gbk') + arr_index[i].fid)		#[p.fname,p.fid, p.fcursor, p.daycount]
	
		self.arr_index = arr_index
		
		arr_index = None

	def __init__(self):
		self.init_tkgui()

any = ui_tk()


