from skymapper.analyze.an_tools import lam_dict_to_array, save_converted_array
import cPickle as pickle

dict_name='lambda_dict_date1_s4_w1'
array_savename= 'array_date1_s4_w1_test'

dict1= pickle.load( open( dict_name ,'rb'))
array1 = lam_dict_to_array(dict1)
save_converted_array(array1, array_savename)


