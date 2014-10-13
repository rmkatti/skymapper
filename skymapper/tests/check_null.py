import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import healpy as hp
import skymapper.gen_maps.SkyMap as SkyMap
from skymapper.analyze.an_tools import find_missed
from skymapper.visualize.plot_points import rad_plot_points
import itertools
import cPickle as pickle

def check_null(lambda_dict_in):
    lambda_dict= pickle.load(open(lambda_dict_in, "rb"))
    list_in = list( itertools.chain(*lambda_dict.values() ))

    null_list=find_missed(list_coords=list_in, nside=2**9, theta_lim=pi/16)
    
    list2=list(map(tuple, null_list))
    rad_plot_points(list2)
    plt.show()


if __name__=='__main__':
    check_null('/home/rmkatti/skymapper/skymapper/data/lambda_dict_null_prac')
