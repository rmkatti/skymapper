"""
First allsky survey

"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from skymapper.visualize.SkyPlots import SkyPlots2
from skymapper.gen_maps.SkyMap import SkyMap
from skymapper.scans.allsky.read_in import read_in_date
from skymapper.visualize.redundancy_funcs import *

import numpy as np
from numpy import pi
import time

def allsky_survey(pointing_file, save_suffix):
    dir= os.path.dirname(__file__)
    savedir = os.path.join(dir, '../../data/allsky_test/')

    # FOV Dimensions
    #FOV_Dim=(2048*6.2/3600.0)*(pi/180.0) # Base Dimension
    FOV_Dim=3.52 * pi/180.0
    FOV_phi=FOV_Dim*2
    FOV_theta=FOV_Dim
    Nstrip=21 # Number of strips on each band of FOV 
    skymap = SkyMap(nside=2**9,LVF_theta=FOV_theta, LVF_phi=FOV_phi, cap_theta=pi) 

    pointings1 = read_in_date(pointing_file)
    
    days = np.unique(pointings1[:,0])
 
    # Initializations
    skyplot1=SkyPlots2()
    fig_sub, ax_sub= plt.subplots(3, 4, subplot_kw=dict(projection="mollweide"))        
    sub_ind=0
    subplot_days=[91,182,273,365]
    plot_days=[1,2,91,182,273,365]
    plot_lambda_ranges=[(.75,2.34),(.75,.76),(1.30,1.33),(2.26,2.34)]


    for day in days:
        points_in=map(tuple, pointings1[ pointings1[:,0]==day, 1:4] )

        for i, tupler in enumerate(points_in):
            print "day:%s, step:%s" %(day, i)
            skymap.make_dicts(day, tupler )

        if day in plot_days:
            for j,tupler in enumerate(plot_lambda_ranges):
                fig1, ax1= plt.subplots(1,1, subplot_kw=dict(projection="mollweide"))        
                redu_mat2, redu_dict2 = redu_data(skymap.lambda_dict, lambda_min=tupler[0] ,lambda_max=tupler[1])
                
                scat, Nhits=redu_allsky( ax1, redu_mat2, redu_dict2)

                fig1.colorbar(scat)
                fig1.set_size_inches(20,10)
                fig1.suptitle("Day %s, Nhits=%s, [%s, %s]" %(day, Nhits, tupler[0], tupler[1]) )        

                savename2="allsky_3_fullrot_%s_%s" %(day,tupler)
                plt.savefig( savedir + "%s.png" %(savename2) )   


        if day in subplot_days:
            redu_mat1, redu_dict1=redu_data(skymap.lambda_dict, .75, 5)
            for j in [0,1,2]:
                redu_allsky( ax_sub[j,sub_ind], redu_mat1, redu_dict1)
            sub_ind+=1

    subplot_proposal1( fig_sub, ax_sub)
    fig_sub.savefig( savedir + "%s.png" %("MultiPanel_allsky_3") )   
    
    # Save Dictionary
    skymap.save_lambda_dict(save_suffix)

 
if __name__=='__main__':
#    allsky_survey('/home/rmkatti/skymapper/skymapper/data/all_sky_days.txt', 'test_out')
#    allsky_survey('/home/rmkatti/skymapper/skymapper/data/test_2000', 'test_out')
    dir= os.path.dirname(__file__)    
    pointfile = os.path.join(dir, '../../data/all_sky_days.txt')

    time1=time.time()
    allsky_survey( pointfile, 'check_RA_vals')
    time2=time.time()
    print "Time Elapsed: %s" %(time2-time1)
