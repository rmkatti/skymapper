from skymapper.analyze.an_tools import lam_dict_to_array, save_converted_array
import cPickle as pickle
import os


dict_name_path='./lambda_dict_deep_date2'
dir = os.path.dirname(__file__)
dict_name = os.path.join(dir, dict_name_path)

array_savename= 'array_deep_date2'

dict1= pickle.load( open( dict_name ,'rb'))
print "Pickle Loaded"

array1 = lam_dict_to_array(dict1)
print "Array Converted"

save_converted_array(array1, array_savename)


