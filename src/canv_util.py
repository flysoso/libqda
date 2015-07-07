class canvAxis:
	def __init__(self, canv, border, arr_area):
		self.border = border
		self.wid = int(canv['width']) - 2 * border
		self.hei = int(canv['height']) - 2 * border
		self.arr_area = arr_area
		self.dx = float(self.wid) / (arr_area[1] - arr_area[0])
		self.dy = float(self.hei) / (arr_area[3] - arr_area[2])
	def to_canv_xy(self,x,y):
		x = x - self.arr_area[0]
		y = y - self.arr_area[2]
		return [self.border + self.dx * x , self.border + (self.hei - self.dy * y)]
	def to_real_xy(self,x,y):
		return [(x - self.border) / self.dx, \
				((self.hei - y) - self.border) / self.dy]

def canv_draw_stline( canv, arr, fixstyle = 0, restrict_time = []):

	#print "------canv:"
	#print canv

	# get min and max
	
	arx_max = -9999
	arx_min = 9999
	ary_min = 9999
	ary_max = -9999
	
	for i in range(0, len(arr)):
			
			arx_max = max(arx_max, arr[i][0])
			arx_min = min(arx_min, arr[i][0])
			
			ary_max = max(ary_max, arr[i][1])
			ary_min = min(ary_min, arr[i][1])

	#4749 ~ -3299

	if (fixstyle) :
		#arx_max = 4749
		#arx_min = -3299
		ary_min = 0
		ary_max = fixstyle
	print "   canv_util, reporting_line_data"
	print "      arX:"
	print "         " + str(["%.2f" %arx_min, "%.2f" %arx_max])
	print "      arY:"
	print "         " + str(["%.2f" %ary_min, "%.2f" %ary_max])
	print "      years_to_2000:"
	print "         " +  "%.2f" % ( arx_min / 365.24) + " ~ " + "%.2f" % (arx_max/365.24)
			
	#restrict_time = [0,300]
	if restrict_time == []:
		i1 = 0
		i2 = len(arr) -1
	else:
		i1 = restrict_time[0];
		i2 = i1 + 1;
		for i in range(0, len(arr)-1):
			if arr[i][0] < restrict_time[0]:
				i1 = i
			if arr[i][1] <= restrict_time[1]:
				i2 = i
			arx_min = arr[i1][0]
			arx_max = arr[i2][0]
		print "  restricted"
		print "    " + str([i1,i2])
	
	axi = canvAxis(canv , border = 44, arr_area = [arx_min, arx_max, ary_min, ary_max])

	canv.create_rectangle(-11,-11,2000,1000, fill="black")  

	test=0
	
	clr_year = []
	for i in range(1,5):
		clr_year.append("green")
		clr_year.append("green")
		clr_year.append("yellow")
		clr_year.append("orange")
		clr_year.append("orange")
		clr_year.append("yellow")
		clr_year.append("white")
		clr_year.append("white")
		clr_year.append("yellow")
		clr_year.append("blue")
		clr_year.append("blue")
		clr_year.append("yellow")
	
	for i in range(-10,+20):
		year_x = i * 365.24
		cx = axi.to_canv_xy(year_x, 1)
		cx = cx[0]
		#canv.create_line(cx,0,cx,1000, fill = clr_year[i + 7])
	
	#cx = axi.to_canv_xy(0, 1)[0]
	#print "ss eaf "
	#print cx
	#canv.create_line(cx,0,cx+100,1000, fill = "white")
	
	for i in range(i1,i2):
		cxy = axi.to_canv_xy(arr[i][0],arr[i][1])	
		cxy2 = axi.to_canv_xy(arr[i+1][0], arr[i+1][1])
		if (test):
			print "arx,ary:"
			print arx
			print ary
		if cxy[1] < cxy2[1]:
			clr = "green"	#fall
		else:
			clr = "red"		#raise
		canv.create_line(cxy[0],cxy[1],cxy[0],cxy2[1], fill = clr)
		
	arx = None
	ary = None
	