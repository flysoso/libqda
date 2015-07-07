import libqda
import pickle

# assume_delay_of_daily_data calculation suit
# delay_coefficient...



#arr = [p.fname,p.fid, p.fcursor, p.daycount]

# ffi = 0 to len(arr_index)

filteredlist = []

def filteredlist_save_to_file(): # NOT USED!!!
    filteredlist = []
    
    arr_index = libqda.get_all_index_arr()
    
    maxcursor = 107100184
    mincursor = 19993952
    
    for i in range( 0, len(arr_index)  ):
        pp = arr_index[i]
        if pp.fcursor > maxcursor:
            break
        if pp.fcursor > mincursor:
            filteredlist.append(pp)

    outputfile = open('filteredlist.txt', 'wb')
    pickle.dump(filteredlist, outputfile, -1)
    outputfile.close()

def read_list_from_file():
    # get filterdlist from file
    outputfile = open('filteredlist.txt', 'rb')
    filteredlist = pickle.load(outputfile)
    #print filteredlist 
    outputfile.close()
    return filteredlist

def function_123123():
    mr = len(filteredlist)
    maxtest = 5
    test = 0

    for i in range(0, mr):
        for j in range(i+1, mr):
            test += 1
            if test > maxtest:
                return
            ar1 = libqda.get_line_arr(filteredlist[i] )
            ar2 = libqda.get_line_arr(filteredlist[j] )
            
            ar1 = sub_area(ar1)
            ar2 = sub_area(ar2)
            
            mintim1 = ar1[0]
            maxtim1 = ar1[0] + len(ar1[1]) - 1
            
            for tim1 in range( mintim1 , mintim1 ):
                
                mintim2 = ar2[0]
                maxtim2 = ar2[0] + len(ar2[1]) - 1
                
                maxdiss = -999
                
                for dv in range(-60, 0):
                    
                    tim2 = tim1 + dv
                    
                    mintim22 = tim1 + dv
                    maxtim22 = tim1 + dv + 60
                                        
                    if mintim22 < mintim2:
                        continue
                    if maxtim22 > maxtim2:
                        break
                    
                    diss = 0
                    for dv2 in range(0,60):
                        diss = diss + ar1[1][tim1+dv2] - ar2[1][tim2+dv2]
                    
                    maxdiss = max(diss, maxdiss)
                
                print "maxdiss--------------"
                print maxdiss
                    
                    

def sub_area(arr):
    st = arr[0]
    arr_sub = []
    for i in range(0, len(arr)):
        for j in range(1, arr[i][0] - st[0]):
            arr_sub.append(1)       # 1 is m2.op / m1.op assume empty area m2 = m1
        arr_sub.append(arr[i][1] / st[1])
        st = arr[i]
    return [arr[0][0], arr_sub]

libqda.qda_init()
filteredlist = read_list_from_file()
function_123123()

#test sub_area
#print sub_area([[1,4],[2,8],[4,32]])