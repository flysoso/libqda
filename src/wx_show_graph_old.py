#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import random
import math

class PaintWindow(wx.Window):
        def __init__(self, parent, id):
            wx.Window.__init__(self, parent, id)
            self.SetBackgroundColour("Black")
            self.color = "White"
            self.thickness = 1
        
            self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
            self.lines = []
            self.curLine = []
            self.pos = (0, 0)
            self.linedata = []
            self.graph = 0
            self.forceaxis = 0
            self.parent = parent
            self.InitBuffer()
            
            
            #self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            #self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            self.Bind(wx.EVT_MOTION, self.OnMotion)
            self.Bind(wx.EVT_SIZE, self.OnSize)
            self.Bind(wx.EVT_IDLE, self.OnIdle)
            self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        def InitBuffer(self):
            size = self.GetClientSize()

            self.buffer = wx.EmptyBitmap(size.width, size.height)
            dc = wx.BufferedDC(None, self.buffer)
            
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
            self.DrawLines(dc)
            self.reInitBuffer = False
        '''
        def GetLinesData(self):
            return self.lines[:]
        
        def SetLinesData(self, lines):
            self.lines = lines[:]
            self.InitBuffer()
            self.Refresh()
            
        def OnLeftDown(self, event):
            self.curLine = []
            
            self.pos = event.GetPositionTuple()
            self.CaptureMouse()
            
        def OnLeftUp(self, event):
            if self.HasCapture():
                self.lines.append((self.color,
                                   self.thickness,
                                   self.curLine))
                self.curLine = []
                self.ReleaseMouse()
        '''
        def OnMotion(self, event):
            
            cpos = event.GetPositionTuple()
            
            dd = self.current_axis

            # 0, 1,  2,    3,    4,    5,    6,       7
            #[dx,dy, xmin, xmax, ymin, ymax, size[0], size[1]]       
            x1 = float(cpos[0]) / dd[6] * (dd[3] - dd[2]) + dd[2]
            y1 = float(dd[7] - cpos[1]) / dd[7] * (dd[5] - dd[4]) + dd[4]
            
            self.parent.SetTitle( str(['%4.4f'%x1,'%4.4f'%y1])   )
            #event.Skip()
            
        def OnSize(self, event):
            self.reInitBuffer = True
        
        def OnIdle(self, event):
            if self.reInitBuffer:
                self.InitBuffer()
                self.Refresh(False)
        
        def OnPaint(self, event):
            dc = wx.BufferedPaintDC(self, self.buffer)
            
        def SetColor(self, color):
            self.color = color
            self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
            
        def SetThickness(self, num):
            self.thickness = num
            self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        
        def DrawLines(self, dc):

            linedata = self.linedata
            #print linedata;
            xmin = 9999
            xmax = -9999
            ymin = 9999
            ymax = -9999
            for i,j in linedata:
                if xmin > i:
                    xmin = i
                if xmax < i:
                    xmax = i
                if ymin > j:
                    ymin = j
                if ymax < j:
                    ymax = j
                    
            if self.forceaxis:
                q = self.forceaxis
                if q[0]:
                    xmin = q[0]
                if q[1]:
                    xmax = q[1]
                if q[2]:
                    ymin = q[2]
                if q[3]:
                    ymax = q[3]
            
            size = self.GetClientSize()
            
            dx = float(size[0]) / (xmax - xmin)
            dy = float(size[1]) / (ymax - ymin)
            
            self.current_axis = [dx,dy, xmin, xmax, ymin, ymax, size[0], size[1]]
            
            self.pen = wx.Pen('White', 1, wx.SOLID)
            
            dc.SetPen(self.pen)
            
            rec = 0
            px = 0
            py = 0
            px1 = 0
            py1 = 0
            for px,py  in linedata:
                px -= xmin
                py -= ymin
                if rec:
                    dc.DrawLine(px*dx,size[1] - py*dy,px1*dx,size[1] - py1*dy)
                px1 = px
                py1 = py
                rec = 1

class PaintFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Panit Frame", size = (1600, 800))
        self.paint = PaintWindow(self, -1)

def show_graph(linedata, forceaxis = 0, graph = 0):
    app = wx.PySimpleApp()
    frame = PaintFrame(None)
    frame.Show(True)
    frame.paint.linedata = linedata
    frame.paint.graph = graph
    frame.paint.forceaxis = forceaxis
    app.MainLoop()
    
#show_graph([[-983, 15.5], [-982, 17.270000457763672], [-981, 16.989999771118164], [-980, 17.010000228881836], [-977, 20.0], [-976, 21.0]])