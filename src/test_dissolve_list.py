def dissolve_list(mlist):
	rlist = []
	for k in mlist:
		print k
		if type(k) is list:
			rlist = rlist + dissolve_list(k)
		else:
			rlist.append(k)
	return rlist

list1 = [1,2,[1,2],1]
	
print dissolve_list(list1)

'''
Why this Wrong????

def dissolve_list(list):
	rlist = []
	for k in list:
		if k is list:
			rlist = rlist + dissolve_list(k)
		else:
			rlist.append(k)
	return rlist
	
	'''