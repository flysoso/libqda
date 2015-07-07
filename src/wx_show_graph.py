#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import random
import math
import month_ancient

pframe = 0
signcolor_x = 0
signlist_x = []

mousePos = (0,0)
mousePos1 = (0,0)
mousePos0 = (0,0)


# spare space in window so that to see the source/end of line
line_end_spare = 200;

def forceAxis( fa, tup4m):
	if fa:
		print fa, tup4m
		for k in range(0,4):
			if fa[k]:
				tup4m[k] = fa[k]
	return tup4m

def get4m(linedata):
	(xmin,xmax,ymin,ymax) = (9999, -9999, 9999, -9999)
	for i,j in linedata:
		if xmin > i:
			xmin = i
		if xmax < i:
			xmax = i
		if ymin > j:
			ymin = j
		if ymax < j:
			ymax = j
	return (xmin,xmax,ymin,ymax)

def zoom_in_axis(x,y,dd):
	'''
	convert x,y from DC, so that it's coincide to real data
			 0, 1,  2,	3,	4,	5,	6,	   7
			[dx,dy, xmin, xmax, ymin, ymax, size[0], size[1]]	
	'''
	
	dx, dy, xmin, xmax, ymin, ymax, wwid, whei = dd

	maxwid = (xmax - xmin) * dx
	stOffset = (float(mousePos[0]) / wwid) * (maxwid - wwid)
	
	y = whei - y
	x1 = ((float(x) + stOffset) / dx + xmin)
	y1 = (float(y) / dy + ymin)
	
	return [x1,y1]

def zoom_out_axis(x,y,dd):
	'''
	# convert x,y so that it's easy to draw on DC
			# 0, 1,  2,	3,	4,	5,	6,	   7
			#[dx,dy, xmin, xmax, ymin, ymax, size[0], size[1]]	
	'''
	dx, dy, xmin, xmax, ymin, ymax, wwid, whei = dd
	if (dx == 0):
		dx = float(wwid) / (xmax - xmin)
	if (dy == 0):
		dy = float(whei) / (ymax - ymin)

		
	maxwid = (xmax - xmin) * dx
	
	
	global stOffset
	maxwid = maxwid + line_end_spare * 2
	
	stOffset = (float(mousePos[0]) / wwid) * (maxwid - wwid)
	stOffset = stOffset - line_end_spare
	

	x1 = (float(x - xmin) * dx - stOffset)
	y1 = float(y - ymin) * dy
	y1 = whei - y1
	dd[0], dd[1] = dx, dy
	return [int(x1+0.5),int(y1+0.5)]

class PaintWindow(wx.Window):
		def __init__(self, parent, id):
			wx.Window.__init__(self, parent, id)
			self.SetBackgroundColour('#000000')
			self.color = "White"
			self.thickness = 1
		
			self.signcolor_x = 'Yellow'
			self.signlist_x = []
			self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
			self.lines = []
			self.curLine = []
			self.pos = (0, 0)
			self.linedata = []
			self.graph = 0
			self.forceaxis = 0
			self.parent = parent
			self.mousedown = 0
			self.xzoom = 1

			self.InitBuffer()
			
			self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)			
			self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
			self.Bind(wx.EVT_MOTION, self.OnMotion)
			self.Bind(wx.EVT_SIZE, self.OnSize)
			self.Bind(wx.EVT_IDLE, self.OnIdle)
			self.Bind(wx.EVT_PAINT, self.OnPaint)
			
			self.Center()
		
		def InitBuffer(self):
			size = self.GetClientSize()

			self.buffer = wx.EmptyBitmap(size.width, size.height)
			
			dc = wx.BufferedDC(None, self.buffer)
			dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
			dc.Clear()
			self.DrawLines(dc)
			
			self.reInitBuffer = False

		def OnLeftDown(self, event):			
			
			self.curLine = []
			global mousePos0
			global mousePos
			global mousePos1
			mousePos0 = mousePos
			mousePos1 = event.GetPositionTuple()
			
		def OnLeftUp(self, event):
			self.mousedown = 0
			
		def OnMotion(self, event):
			
			cpos = event.GetPositionTuple()   
			
			[x1,y1] = zoom_in_axis(cpos[0],cpos[1], self.current_axis)
			
			month_num = int((x1 - 25) / (365.24 / 12))
			
			self.parent.SetTitle( str(['%4.4f'%x1,'%4.4f'%y1]) + "  month_num = " + str(month_num) + '  month_str = ' + month_ancient.getMonthStr(month_num) )
			
			if event.LeftIsDown():
				global mousePos
				x = mousePos0[0] + float(cpos[0] - mousePos1[0]) / 3
				mousePos = (x,0)
				self.reInitBuffer = True
			
		def OnSize(self, event):
			self.reInitBuffer = True
		
		def OnIdle(self, event):
			if self.reInitBuffer:
				self.InitBuffer()
				self.Refresh(False)
		
		def OnPaint(self, event):
			wx.BufferedPaintDC(self, self.buffer)
		
		def DrawLines(self, dc):

			linedata = self.linedata
			
			#print linedata;
			(xmin,xmax,ymin,ymax) = get4m(linedata)

			xmin,xmax,ymin,ymax = forceAxis(  self.forceaxis,
												[xmin,xmax,ymin,ymax] )
			
			
			# Get hdc Size (pixel)
			size = self.GetClientSize()
			wwidth, wheight= size[0], size[1]
			
			# axis set
			self.current_axis = [2, 0, xmin, xmax, ymin, ymax, wwidth, wheight]
			
			
			# draw rect represent month length
			
			dc.SetPen(wx.Pen(wx.ColorRGB(0x0F1F)))
			dc.SetBrush(wx.Brush('0xFF0000', wx.TRANSPARENT ))
			
			for ff in range(-120,200):
				px1 = zoom_out_axis(0 + 25 + (ff*365.24/12), 0, self.current_axis)[0]
				px2 = zoom_out_axis(0 + 25 + ((ff+1)*365.24/12), 0, self.current_axis)[0]
				if ff % 12 == 8:
					dc.SetPen(wx.Pen(wx.ColorRGB(0xFF0F1F)))
				else:
					dc.SetPen(wx.Pen(wx.ColorRGB(0x000F1F)))
				dc.DrawRectangle(px1,10,px2-px1,1000)
			
			dc.SetPen(wx.Pen(wx.ColorRGB(0xFFFFFF)))
			
			if not linedata:
				return
			
			rec,px,py,px1,py1 = 0,0,0,0,0
			
			px1, py1 = linedata[0]
			[px1,py1] = zoom_out_axis(px1,py1, self.current_axis)
			
			for px,py  in linedata:
				[px,py] = zoom_out_axis(px,py, self.current_axis)
				dc.DrawLine(px,py,px1,py1)
				px1,py1 = px,py
				

class PaintFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, "Panit Frame", size = (1600, 800))
		self.paint = PaintWindow(self, -1)
		self.Center();

def show_graph(linedata, forceaxis = 0, graph = 0, xzoom = 1):
	app = wx.PySimpleApp()
	frame = PaintFrame(None)
	frame.Show(True)
	
	global pframe
	
	pframe = frame.paint
	
	pframe.linedata = linedata
	pframe.graph = graph
	pframe.forceaxis = forceaxis
	pframe.signlist_x = signlist_x
	pframe.signcolor_x = signcolor_x
	pframe.xzoom = xzoom
	
	app.MainLoop()

def set_sign_x(signlist):
	global signcolor_x, signlist_x
	signcolor_x = 'Yellow'
	signlist_x = signlist;
	
if __name__ == '__main__':
	show_graph([[-983, 15.5], [-982, 17.270000457763672], [-981, 16.989999771118164], [-980, 17.010000228881836], [-977, 20.0], [-976, 21.0]])