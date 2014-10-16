"""
First allsky survey

"""

from skymapper.visualize.SkyPlots import SkyPlots2
from skymapper.gen_maps.SkyMap import SkyMap
from skymapper.scans.allsky.read_in import read_in_date

import numpy as np
from numpy import pi

import matplotlib.pyplot as plt


def allsky_survey(pointing_file, save_suffix):

    # FOV Dimensions
    FOV_Dim=(2048*6.2/3600)*(pi/180) # Base Dimension
    FOV_phi=FOV_Dim*2
    FOV_theta=FOV_Dim
    Nstrip=21 # Number of strips on each band of FOV 
    skymap = SkyMap(nside=2**8,LVF_theta=FOV_theta, LVF_phi=FOV_phi, cap_theta=pi, Nstrips=Nstrip, lambda_min1=.75, lambda_min2=1.25) 

    pointings1 = read_in_date(pointing_file)
    

    days = np.unique(pointings1[:,0])
   
    skyplot1=SkyPlots2()
    for day in days:
        points_in=map(tuple, pointings1[ pointings1[:,0]==day, 1:4] )

        for i, tupler in enumerate(points_in):
            print "day:%s, step:%s" %(day, i)
            skymap.make_dicts(day, tupler )

        fig2, ax2= plt.subplots(2,2)
        mult_ind=0
        #plot_days=[1,2, 91, 182, 273, 365] :
        plot_days=[1,2,3,4]
        plot_lambda_ranges=[(.75,5),(.75,.76),(1.25,1.26),(1.98,2.00)]

        if day in plot_days :
            for j,tupler in enumerate(plot_lambda_ranges):
                #fig1=plt.figure()
                skyplot1.redundancy_plot(skymap.lambda_dict, radius_line=pi, lambda_min=tupler[0] ,lambda_max=tupler[1],plot_type='allsky', plot_title="All Sky Hits Map: [%s, %s]" %(tupler[0], tupler[1]) )        
                savename2="allsky_test2_%s_%s" %(day,tupler)
                plt.savefig( "/home/rmkatti/skymapper/skymapper/data/allsky_time/%s.png" %(savename2) )   

                if (day in [1,2,3,4]) and (j==0):
                    ax2[mult_ind]=plt.gca()
                    mult_ind+=1   

    fig2.savefig( "/home/rmkatti/skymapper/skymapper/data/allsky_time/%s.png" %("MultiPanel") )   
    skymap.save_lambda_dict(save_suffix)

 
if __name__=='__main__':
#    allsky_survey('/home/rmkatti/skymapper/skymapper/data/all_sky_days.txt', 'test_out')
#    allsky_survey('/home/rmkatti/skymapper/skymapper/data/test_2000', 'test_out')
    allsky_survey('/home/rmkatti/skymapper/skymapper/data/test_data_2', 'test_out')
    
