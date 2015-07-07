
# -*- coding: cp936 -*-

import struct
import time
import random
import libqda_struct
import math
#import matplotlib.pyplot as plt  


sfday = "ifffffff"
size_of_fday = 32

sfdata = "12s12si"
size_of_fdata = 28

sfhdr = "iii"
size_of_fhdr = 12;

test = 0;

stcount = 0;


#fout = open("E:\dev_python\out.txt","w");

fp = open("E:\\dev\\data.qda","rb");
#fp = open("Z:\\data.qda",'rb');

linedata = []

#hdr, typ, stcount
		
def read_1():
	fp.seek(0)
	fr = fp.read(size_of_fhdr);
	global stcount;
	hdr, typ, stcount = struct.unpack(sfhdr, fr);
	if(test):
		print "Header found : " + str(stcount);

def read_2():

	mdata = libqda_struct.fdata();
	mdata.fcursor = fp.tell();
	
	fr = fp.read(size_of_fdata);
	fid = '';
	fid, fname, daycount = struct.unpack(sfdata, fr);
	
	fname = fname.replace('\0', '')
	fid = fid.replace('\0', '')
	
	mdata.pars(fid,fname,daycount);
	return mdata;

def read_3():
	fr = fp.read(size_of_fday);
	ftime, op, hig, low, cl, vol, amount, dealcount = struct.unpack(sfday, fr);
	mdata = libqda_struct.fdaydata();
	mdata.pars(ftime, op, hig, low, cl, vol, amount, dealcount);
	return mdata;

def skipcur(p): #warp to the fid that is behind p.fid
	fp.seek( fp.tell() + size_of_fday * p.daycount );
	if(test):
		print "...Skipped to " + str( fp.tell() );

def output_index():
	for i in range(0,stcount): #range(0,stcount)
		p = read_2();
		#fout.write(p.fname + " " + str(p.fcursor) + " " + str(p.daycount) + " " + str(p.fid) + "\n");
		skipcur(p);
		
def get_stock_info_list(filter = 0):
	return get_all_index_arr(filter=0)

def get_all_index_arr(filter = 0):  # must be called right after read_1
	arr_all=[]
	
	print "--libqda: Auto Filtered data which daycount <= some."
	
	for i in range(0,stcount): #range(0,stcount)
		
		filterThis = 0;
		
		p = read_2();
		#fout.write(p.fname + " " + str(p.fcursor) + " " + str(p.daycount) + " " + str(p.fid) + "\n");
		arr = p
					# this is the arr_index format

		if (filter == 1):
			if (p.daycount < 3650): filterThis = 1
		
		if (filter == 2):
			try:
				id1 = int(p.fid[2:])
			except:
				id1 = 0
			if p.fid[0:2] == 'SH':
				if id1 < 600000:	filterThis = 1
				if id1 > 900999:	filterThis = 1
			else:
				if id1 > 300199:	filterThis = 1
				
		
		'''
			各种指数过滤掉
		'''
		for i in [u'\u503a', "GC", "RC"]:
			if p.fname.decode('gbk').find(i) != -1 :
				filterThis = 1
				break
		
		if (filterThis == 0):
			arr_all.append(arr)
		
		skipcur(p);
		
	return arr_all
		
def output_all_date_of(p):
	fp.seek(p.fcursor);
	read_2();
	for i in range(0, p.daycount):
		q = read_3();
		print time.ctime(q.ftime);
		
def get_by_cursor(q ,preload_enabled = 0):
	
	for i in linedata:
		if i[0] == q:
			print "preloaded-----------"
			return i[2]
	
	fp.seek(q);
	return read_2();
		#print fp.tell();	# return cursor position on the file 'fp'
def get_line_arr_fdaydata(p, preload_enabled = 0):  #current stock day lines

	
	xx=[]
	
	fp.seek(p.fcursor)
	read_2();

	for i in range(0, p.daycount):
		q = read_3();
		xx.append(q); #10956 is {{{ time.mktime(2000,1,1) / 86400 }}}
	
	return xx;

def dayline_plot_data(dayline):
	xx = []
	for k in dayline:
		mt = k.op
		daynum = k.ftime / 86400 - 10956;
		xx.append([daynum, mt])
	return xx;
	
def get_line_arr_in_range(p, range1=[0,0]):

	xx=[]
	
	fp.seek(p.fcursor)
	read_2();
	
	for i in range(0, p.daycount):
		q = read_3();		
		mt = q.op
		daynum = q.ftime / 86400 - 10956;
		if daynum > range1[0]:
			xx.append([daynum, mt]);
		if daynum > range1[1]:
			break
	
	return xx;

def get_line_arr(p, test = 0, preload_enabled = 0):  #current stock day lines
	
	#if preload:
		# define linedata[0] = [p, fd ,[fdd1,fdd2,fdd3...]] // fd = fdata, fdd=fdaydata
	for i in range(0, len(linedata)):
		#print linedata[i][0]
		if linedata[i][0] == p.fcursor:
			print "data loaded from preload_data"
			return linedata[i][1]
	
	xx=[]
	
	fp.seek(p.fcursor)
	read_2();
	
	if test:
		print p.fname.decode('gbk') + " - " + str(p.fid)
		print "   libqda_exporting_daily_data"
	
	
	for i in range(0, p.daycount):
		q = read_3();		
		mt = q.op
		if 1:
			xx.append([q.ftime / 86400 - 10956, mt]); 
			#10956 is {{{ time.mktime(2000,1,1) / 86400 }}}

	if preload_enabled:
		linedata.append([p.fcursor, xx, p])
	
	return xx;
		
def output_grid_of(p):
	fp.seek(p.fcursor);
	pp = read_2();
	print "current: " + pp.fname
	arr = get_line_arr(p)
	xx = arr[0]
	yy = arr[1]
	plt.plot(xx,yy);
	plt.show();


def test1():
	qda_init()
	
	# after init, it's proper time to run "read_2", after that, "read_3" by certain times
	
	p =  get_by_fid(107139060);
	output_grid_of(p);
	#output_all_date_of(p);
	raw_input("\nPress Any Key ...");
	
def qda_init():
	
	read_1();

print "this is libqda on the line"