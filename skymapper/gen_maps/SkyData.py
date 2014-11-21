'''Class for handling skypixel data'''

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import collections
from numpy import pi
import healpy as hp
import time
import random
from skymapper.visualize.plot_points import moll_plot

class SkyData(object):
    ''' Initialize SkyData() with 1-D numpy arrays of the theta and phi values of
        your sky pixel centers (theta_in, phi_in). The arrays should be the 
        same length and 
        correspond to the (theta, phi) pairs of your sky pixel centers.

        lambda_in is the 1-D array of wavelength values your FOV observes at.

        self.sky_table format:
             cols: 'theta', 'phi', 'lambda_0',...'lambda_n' '''

    def __init__(self, theta_in, phi_in, lambda_in):
        '''theta_in, phi_in numpy arrays of same length, 
           lambda_in numpy array'''

        self.thetas=theta_in
        self.phis=phi_in
        self.lambdas=lambda_in
        self.sky_df= self.make_sky_df(theta_in, phi_in, lambda_in)

    def make_sky_df(self, theta_vals, phi_vals, lambda_vals):
        '''Reads in 1D arrays each of theta_in, phi_in, and lambda_vals. Returns
        pandas multidimensional index dataframe with top-level index theta_vals,
        next-level index phi_vals, and bottom level index lambda_vals. For
        each triple of index vals (thetai,phii,lambdai), there is a single
        field corresponding to number of hits'''

        if len(theta_vals)!=len(phi_vals):
            raise TypeError("Unequal input vectors:len(theta_vals) %s, len(phi_vals) %s)" %(len(theta_vals), len(phi_vals)))

        index_row=len(theta_vals)*len(lambda_vals)
        index_col = 3
        index_mat=np.empty([index_row, index_col])*np.nan
 
        index_mat[:,0]=np.repeat(theta_vals, len(lambda_vals))
        index_mat[:,1]=np.repeat(phi_vals, len(lambda_vals))  
        index_mat[:,2]=np.tile(lambda_vals, len(theta_vals))
        
        return pd.DataFrame(np.zeros(index_mat.shape[0]), index=pd.MultiIndex.from_arrays(index_mat.T))

    def increment_hit(self, list_in):
        '''Add one to hits value given list of [(theta1, phi1,lambda_1),
        (theta2,phi2,lambda_val2)...] '''

        self.sky_df.ix[list_in]+=1

    def get_hits(self, list_in):
        '''Return hits number at theta_val, phi_val, and lam_val'''

        return self.sky_df.ix[list_in]
        
    def least_hits_array(self):
        '''Returns numpy array with col: [thetas, phis, least_hits] '''

        grouped=self.sky_df.groupby(level=[0,1]).min()
        least_array=grouped.reset_index().values
        least_array=least_array[least_array[:,2]>0]
        return least_array

    def sum_hits_array(self):
        '''Returns numpy array with col: [thetas, phis, sum_hits] '''

        grouped=self.sky_df.groupby(level=[0,1]).sum()
        least_array=grouped.reset_index().values
        least_array=least_array[least_array[:,2]>0]
        return least_array

    def lambda_counts_sum(self):
        '''Returns numpy array with col: [thetas, phis, sum_lambda_hits] '''

        grouped=self.sky_df.groupby(level=2).sum()
        lambda_array=grouped.reset_index().values
        return lambda_array

    def lambda_counts_least(self):
        '''Returns numpy array with col: [thetas, phis, least_hits] '''

        grouped=self.sky_df.groupby(level=2).min()
        lambda_array=grouped.reset_index().values
        return lambda_array



if __name__=='__main__':
    
    # Example sky discretization. Discretizes sky into 12*(2**8)**2 pixels
    nside=2**8
    npix=12*nside**2 
    ind=np.arange(npix) # index of pointings
    pix_array=np.array( hp.pix2ang(nside, ind)).T 
    theta_in1=pix_array[:,0]
    phi_in1=pix_array[:,1]
    lambda_in1 = np.linspace(.75,2.4,41)
    print len(phi_in1), len(theta_in1)

    time6=time.time() 
    sky_dat1=SkyData(theta_in1, phi_in1, lambda_in1)
    time7=time.time()   
    print ("Time to make data frame: %s" %(time7-time6))
    print sky_dat1.sky_df.shape

    interim_list=[]
    timer=0
    time1=time.time()
    #for i in range(100):
    #    rin=random.randint(0,len(theta_in1))
    #    thet_rand, phi_rand, lam_rand = [theta_in1[rin], phi_in1[rin], random.choice(lambda_in1)]
    #    interim_list.append((thet_rand,phi_rand,lam_rand))       

    interim_list=[]
    timer=0
    time1=time.time()
    for j in range(5):
        for i, lambdai in enumerate(lambda_in1):
            tupleri=(theta_in1[j], phi_in1[j], lambda_in1[i])
            interim_list.append(tupleri)       


    ex_list=[interim_list[0]]
    
    print sky_dat1.get_hits(ex_list)
    time3=time.time()           
    sky_dat1.increment_hit(ex_list)
    time4=time.time()        
    print sky_dat1.get_hits(ex_list)
    print "Time of Execution Ex: %s" %(time4-time3)
  
    
    print sky_dat1.get_hits(interim_list)
    time3=time.time()           
    sky_dat1.increment_hit(interim_list)
    time4=time.time()        
    print "Time of Execution Interim: %s" %(time4-time3)
    print sky_dat1.get_hits(interim_list)

    least_array1= sky_dat1.least_hits_array()
    print least_array1

    thetas=least_array1[:,0]
    phis=least_array1[:,1]
    hits= least_array1[:,2]    
    moll_plot(thetas, phis, hits, "least_allsky", "least_allsky_ex")
