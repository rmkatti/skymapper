"""
deepsky survey

"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from skymapper.visualize.SkyPlots import SkyPlots2
from skymapper.gen_maps.SkyMap import SkyMap
from skymapper.scans.deepsky.gen_deepsky import *
from skymapper.visualize.redundancy_funcs import *


import numpy as np
from numpy import pi
import time

def deepsky_date_survey(save_suffix):

    dir= os.path.dirname(__file__)
    savedir = os.path.join(dir, '../../data/deepsky_test/deep_doubleout_3/')


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
    skymap = SkyMap(nside=2**10,LVF_theta=FOV_theta, LVF_phi=FOV_phi, cap_theta=15*pi/180) 
    skyplot1=SkyPlots2()
    fig_sub, ax_sub= plt.subplots(1, 4, subplot_kw=dict(polar=True))        
    sub_ind=0
    subplot_days=[2, 90, 182, 364]
    #subplot_days=[1,3,7,10]
    plot_days=[1,2,3,4,5,6,7,8, 90, 182, 270, 364]
    #plot_days=[1,2,3,7,10]
    plot_lambda_ranges=[(.75,2.34),(.75,.76),(1.30,1.33),(2.26,2.34)]


    for day in days:
        points_in=map(tuple, pointings1[ pointings1[:,0]==day, 1:4] )

        for i, tupler in enumerate(points_in):
            print "day:%s, step:%s" %(day, i)
            skymap.make_dicts(day, tupler )

        if day in plot_days:
            for j,tupler in enumerate(plot_lambda_ranges):
                fig1, ax1= plt.subplots(1,1, subplot_kw=dict(polar=True))        
                redu_mat2, redu_dict2 = redu_data(skymap.lambda_dict, lambda_min=tupler[0] ,lambda_max=tupler[1])
                
                scat, Nhits=redu_deepsky( ax1, redu_mat2, redu_dict2)

                fig1.colorbar(scat)
                fig1.set_size_inches(20,10)
                fig1.suptitle("Day %s, Nhits=%s, [%s, %s]" %(day, Nhits, tupler[0], tupler[1]) )        

                savename2="double_out3_%s_%s" %(day,tupler)
                plt.savefig( savedir + "%s.png" %(savename2) )   


        if day in subplot_days:
            redu_mat1, redu_dict1=redu_data(skymap.lambda_dict, .75, 5)
            redu_deepsky( ax_sub[sub_ind], redu_mat1, redu_dict1)
            sub_ind+=1

    subplot_proposal1( fig_sub, ax_sub)
    fig_sub.savefig( savedir + "%s.png" %("MultiPanel_deep_1") )   
    
    # Save Dictionary
    #skymap.save_lambda_dict(save_suffix)

def gen_deepskydate1_points():

    FOV_Dim=(2048*6.2/3600)*(pi/180) # Base Dimension
    FOV_phi=FOV_Dim*2
    FOV_theta=FOV_Dim
    Strip_width= FOV_Dim/24
    cent_line_dist= FOV_Dim/2.0
    out_line_dist= (3.0/2)*FOV_Dim

    #Num_long=24
    #Num_out=6
    #theta_long_1=FOV_Dim
    #theta_long_2=-FOV_Dim
    #theta_out_1= 6*Strip_width
    #theta_out_2=-6*Strip_width

   # Num_long=48.0
   # Num_out=12.0
   # theta_long_1=0
   # theta_long_2=0
   # theta_out_1= 0
   # theta_out_2=0

    point_matr=np.array([])

    days= range(1,366)
    #days=[1,2,3,4,5,6,7,8,9,10]
    #days=[1,2,3]
    for day in days:
        flag=day % 8

        if flag==1:
            Num_long=24
            Num_out=0

            theta_long_1=FOV_Dim
            theta_long_2=0
            
            theta_out_1=0
            theta_out_2=0

        if flag==2:
            Num_long=24
            Num_out=0

            theta_long_1=0
            theta_long_2=-FOV_Dim

            theta_out_1=0
            theta_out_2=0

        if flag==3:
            Num_long=0
            Num_out=24
  
            theta_out_1=FOV_Dim
            theta_out_2=0
         
            theta_long_1=0
            theta_long_2=0  

        if flag==4:
            Num_long=0
            Num_out=24

            theta_out_1=0
            theta_out_2=-FOV_Dim        

            theta_long_1=0
            theta_long_2=0  

        if flag==5:
            Num_long=0
            Num_out=24

            theta_out_1=FOV_Dim
            theta_out_2=0        

            theta_long_1=0
            theta_long_2=0  
 
        if flag==6:
            Num_long=0
            Num_out=24

            theta_out_1=0
            theta_out_2=-FOV_Dim        

            theta_long_1=0
            theta_long_2=0
  
        if flag==7:
            Num_long=0
            Num_out=24

            theta_out_1=FOV_Dim
            theta_out_2=0        

            theta_long_1=0
            theta_long_2=0  
 
        if flag==0:
            Num_long=0
            Num_out=24

            theta_out_1=0
            theta_out_2=-FOV_Dim        

            theta_long_1=0
            theta_long_2=0  
   
        #phi= day*2*pi/len(days)
        phi= day*2*pi/365
         
        list1= gen_deep3(-cent_line_dist, phi,theta_long_1,theta_long_2, Num_long)
        list2= gen_deep3(cent_line_dist, phi, theta_long_1, theta_long_2 , Num_long)
        list3= gen_deep3(-out_line_dist, phi, theta_out_1, theta_out_2, Num_out  )
        list4= gen_deep3(out_line_dist, phi, theta_out_1, theta_out_2, Num_out  )       

        point_list_i= points_to_nparray(day, list1+list2+list3+list4)

        if point_matr.size==0:
            point_matr = point_list_i

        elif point_matr.size > 0:
            point_matr = np.append(point_matr, point_list_i, axis=0)

    return point_matr

 
if __name__=='__main__':

    time1=time.time()
    deepsky_date_survey( 'deep_doubleout')

    time2=time.time()
    print "Time Elapsed: %s" %(time2-time1)
