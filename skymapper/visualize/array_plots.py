import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from skymapper.visualize.redundancy_funcs import array_mean_std_plot


if __name__=='__main__':

    array_mean_std_plot('array_test_FOM.npy', './')

    
