"""
deepsky survey

"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from skymapper.visualize.SkyPlots import SkyPlots2
from skymapper.gen_maps.SkyMap2 import SkyMap2
from skymapper.scans.deepsky.gen_deepsky import *
from skymapper.visualize.redundancy_funcs import *
from skymapper.visualize.plot_points import poll_plot

import numpy as np
from numpy import pi
import time

def deepsky_date_survey(save_suffix):

    dir= os.path.dirname(__file__)
    savedir = os.path.join(dir, '../../data/deepsky_test/deepsky_figure/')


    # FOV Dimensions
    FOV_Dim=(2048*6.2/3600)*(pi/180) # Base Dimension
    FOV_phi=FOV_Dim*2
    FOV_theta=FOV_Dim

    # Pointings

    pointings1= gen_deepskydate1_points()

    #pointings1=np.array([[1.0, pi/36,0, 0],
    #                    [1.0, pi/62, 0, 0]])

    days = np.unique(pointings1[:,0])
   
    # Initializations
    skymap = SkyMap2(nside=2**10,LVF_theta=FOV_theta, LVF_phi=FOV_phi, cap_theta=12*pi/180) 
   
    sum_plot_days=[2,10, 92, 182,274]
    least_plot_days=[30,92, 182,184, 274]

    for day in days:
        points_in=map(tuple, pointings1[ pointings1[:,0]==day, 1:4] )

        for i, tupler in enumerate(points_in):
            print "day:%s, step:%s" %(day, i)
            skymap.make_dicts(day, tupler )

            if (day in least_plot_days) & (i==0):
                least_hits_arr=skymap.least_hits()

                theta_in=least_hits_arr[:, 0]
                phi_in=least_hits_arr[:, 1]
                hits_in=least_hits_arr[:, 2]
                poll_plot(theta_in, phi_in, hits_in , "least_deep: Day %s"%(day), "least_deep_fig2_%s"%(day-1))

            #if (day in sum_plot_days) & (i==0):
             #   sum_hits_arr=skymap.sum_hits()

             #   theta_in=sum_hits_arr[:, 0]
             #   phi_in=sum_hits_arr[:, 1]
             #   hits_in=sum_hits_arr[:, 2]
             #   poll_plot(theta_in, phi_in, hits_in , "sum_deep: Day %s"%(day), "sum_deep_fig_%s"%(day))


    least_hits_arr=skymap.least_hits()
    theta_in=least_hits_arr[:, 0]
    phi_in=least_hits_arr[:, 1]
    hits_in=least_hits_arr[:, 2]
    poll_plot(theta_in, phi_in, hits_in , "least_deep: Day %s"%("FINAL"), "least_deep_fig2_%s"%("FINAL"))


    #sum_hits_arr=skymap.sum_hits()
    #theta_in=sum_hits_arr[:, 0]
    #phi_in=sum_hits_arr[:, 1]
    #hits_in=sum_hits_arr[:, 2]
    #poll_plot(theta_in, phi_in, hits_in , "sum_deep: Day %s"%("FINAL"), "sum_deep_fig_%s"%("FINAL"))



def gen_deepskydate1_points():

    FOV_Dim=(2048*6.2/3600)*(pi/180) # Base Dimension
    FOV_phi=FOV_Dim*2
    FOV_theta=FOV_Dim
    Strip_width= FOV_Dim/24.0
    cent_line_dist= FOV_Dim/2.0
    out_line_dist= (3.0/2)*FOV_Dim

    #Num_long=24
    #Num_out=6
    #theta_long_1=FOV_Dim
    #theta_long_2=-FOV_Dim
    #theta_out_1= 6*Strip_width
    #theta_out_2=-6*Strip_width

    Num_long=48.0
    Num_out=12.0
    theta_long_1=FOV_Dim
    theta_long_2=-FOV_Dim
    theta_out_1= 3*Strip_width
    theta_out_2=-3*Strip_width

    point_matr=np.array([])

    days= range(2,366,2)
    #days=[1,2,3,4,5,6,7,8,9,10]
    #days=[1,2,3]
    for day in days:

        #phi= day*2*pi/len(days)
        phi= day*2*pi/365
         
        list1= gen_deep3(-cent_line_dist, phi,theta_long_1, theta_long_2, Num_long)
        list2= gen_deep3(cent_line_dist, phi, theta_long_1, theta_long_2 , Num_long)
        list3= gen_deep3(-out_line_dist, phi, theta_out_1, theta_out_2, Num_out  )
        list4= gen_deep3(out_line_dist, phi, theta_out_1, theta_out_2, Num_out  )       
        list3 *=2
        list4 *=2

        point_list_i= points_to_nparray(day, list1+list2+list3+list4)

        if point_matr.size==0:
            point_matr = point_list_i

        elif point_matr.size > 0:
            point_matr = np.append(point_matr, point_list_i, axis=0)

    return point_matr

 
if __name__=='__main__':

    time1=time.time()
    deepsky_date_survey( 'deep_date2')

    
    time2=time.time()
    print "Time Elapsed: %s" %(time2-time1)
