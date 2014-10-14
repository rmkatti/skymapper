from skymapper.visualize.plot_points import moll_plot_points

from skymapper.analyze.an_tools import find_missed
import skymapper.gen_maps.SkyMap as SkyMap
import healpy as hp

import itertools
import cPickle as pickle
import time
import numpy as np
from numpy import pi


def check_null(lambda_dict_in):
    time1=time.time()

    lambda_dict= pickle.load(open(lambda_dict_in, "rb"))
    print "lambda_dict loaded"

    #list_in = list( itertools.chain(*lambda_dict.values() ))
    list_in=lambda_dict[lambda_dict.keys()[0]]

    null_list=find_missed(list_coords=list_in, nside=2**8, theta_lim=pi)    
    list2=list(map(tuple, null_list))
    moll_plot_points(list2,"fullsky2", savename="allsky")
    

    time2=time.time()
    print "Program Duration = %s" %(time2-time1)    

if __name__=='__main__':
    check_null('/data/rmkatti/lambda_dict_allsky_fullsky2')
