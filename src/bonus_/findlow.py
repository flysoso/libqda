f = open("Z:\\python\\list.txt", 'r')

arr = []

while 1:
	s = f.readline()
	if not s: break
	if len(s) > 3:
		arr.append(s.split(' '))
	#print s.split(' ')
	
#print arr[0][2]

arr = sorted(arr, key = lambda q: q[2])

recomm = []

for i in range(0, len(arr)-1):
	if arr[i][2] == arr[i+1][2]:
		print arr[i][2]
		print arr[i+1][2]
		recomm.append(i)
	
print 'recommended...........'
for i in range(0,3): print

for i in recomm:
	if arr[i][12] != '0.00-0.00':
		print arr[i][2], arr[i][3].decode('gbk')
	
raw_input()