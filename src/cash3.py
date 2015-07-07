import pickle_util

# this one perform sort of list departed from cash2

def printTheList(result_list):
    for tt in result_list:
        print tt[0].fname.replace('\0',' ')
        print tt[0].fid.replace('\0',' ')
        print tt[1]

result_list = pickle_util.load_arr_from_file("shake.txt")

result_list.sort(key = lambda x: x[1])

printTheList( result_list)