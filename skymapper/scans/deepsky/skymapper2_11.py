import numpy as np
import matplotlib
import matplotlib as mpl
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import healpy as hp
from math import acos, atan2
from numpy import pi, cos, sin
import collections as coll
import json
import time
import cPickle as pickle
from collections import Counter
import subprocess














if __name__=='__main__':

    theta_cap1=np.arccos(1- 100*(pi/180)**2/(2*pi))
    #scan_strat3('scan_strat3')

    #allsky_survey("all_sky2.txt", "allsky_fullsky2")

    # Redundancy Plots
    skyplot1=SkyPlots2()

    print "Unpickling"

    t0=time.time()
    lambda_dict2 = pickle.load(open("lambda_dict_allsky_fullsky2", "rb"))
    t1=time.time()
    print "Unpickling time: %s" %(t1-t0)

    lambda_dict2.keys

    # Allsky survey
    for i, key in enumerate(lambda_dict2.keys()):
        #skyplot1.redundancy_plot(lambda_dict2, radius_line=theta_cap1, lambda_min=tupler[0] ,lambda_max=tupler[1],plot_type='allsky', plot_title="Hits map; lambda [%.2fum,%.2fum)" %( tupler[0], tupler[1]) )        
        #savename2="allsky2_complete_%s" %(i)
        #plt.savefig(savename2)   

        skyplot1.lambda_radial_histogram(lambda_dict2, lambda_min=key, lambda_max=key+.000001)
        savename3="normed_hist%s" %(i)
        plt.savefig(savename3)





