import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from skymapper.visualize.redundancy_funcs import plot_hist


if __name__=='__main__':

    row_id=1000
    array_name= 'saved_array_365.npy'
    title= "Array:%s, Pixel ID: %s" %(array_name, row_id)
    savename= 'hist_%s_%s' %(array_name, row_id)

    plot_hist('saved_array_365.npy', row_id, savename, title)

    
