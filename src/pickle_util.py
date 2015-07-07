import pickle

def arr_save_to_file(arr, filename):
    outputfile = open(filename, 'wb')
    pickle.dump(arr, outputfile, -1)
    outputfile.close()

def load_arr_from_file(filename):
    outputfile = open(filename, 'rb')
    arr = pickle.load(outputfile)
    outputfile.close()
    return arr