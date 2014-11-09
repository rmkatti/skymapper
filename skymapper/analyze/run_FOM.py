from skymapper.analyze.an_tools import FOM_2
import numpy as np

if __name__=='__main__':

   numpy_array=np.load('array_test_FOM_small.npy')

   out_tuple= FOM_2(numpy_array)

   print out_tuple
