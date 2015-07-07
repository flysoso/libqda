from Tkinter import *

class cat_box:
	def __init__(self, msg):
		rt = Tk()
		rt.geometry('600x400')
		label1 = Label(rt, text = msg, justify = "left")
		label1.pack()
		rt.mainloop()

def getcomm(ui, cmd):
	print "this is cat.getcomm"
	cmd = cmd.split(",")
	if cmd[0] == 'df':
		print "cat: fixstyle disabled"
		ui.fixstyle = 0
	if cmd[0] == 'f':
		print "cat: fixstyle enabled"
		if len(cmd) == 1:
			ui.fixstyle = 30
			print "fixstyle max 30 as default"
		else:
			ui.fixstyle = int(cmd[1])
	if cmd[0] == 'dr':
		ui.restrict_time = []
		print "restrict time disabled"
	if cmd[0] == 'r':
		ui.restrict_time = [int(cmd[1]), int(cmd[2])]
		print "restrict time enabled"
	if cmd[0] == 'ref':
		ui.lb1_click(0)
	if cmd[0] == 'cur':
		ui.stat_show(ui.cur)
	if cmd[0] == 'data':
		msgstr = "  ID: " + str(ui.cur_data.fid) + "\n  NAME:" + ui.cur_data.fname.decode("gbk") + "\n  DAYC:" + str(ui.cur_data.daycount)
		mmsg = cat_box(msgstr)
	if cmd[0] == 'xzoom':
		pass
	#print cmd