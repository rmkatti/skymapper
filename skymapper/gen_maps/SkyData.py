'''Class for outputting and inputting skypixel data'''

import pandas as pd
import numpy as np
import collections
from numpy import pi
import healpy as hp
import time

class SkyData(object):
    '''self.sky_table format: cols: 'theta', 'phi', 'lambda_0',...'lambda_n' '''

    def __init__(self):
        self.thetas=np.array([])
        self.phis=np.array([])
        self.lambda_vals2labels=collections.OrderedDict()
        self.lambda_labels2vals=collections.OrderedDict()
        self.sky_table=np.array([])
    
    def set_pix_lambdas(self, theta_in, phi_in, lambda_vals):

        if len(theta_in)!=len(phi_in):
            raise TypeError("Unequal input vectors:len(theta_in) %s, len(phi_in) %s)" %(len(theta_in), len(phi_in)))

        self.make_lambda_lookups(lambda_vals)

        interim_dict={}
        for lambdai in self.lambda_labels2vals.keys():
            interim_dict[lambdai]=np.zeros( len(theta_in) )
        interim_dict['theta']= theta_in
        interim_dict['phi']= phi_in
        
        self.sky_table=pd.DataFrame(interim_dict)

    def increment_hit(self, theta, phi, lambda_val):
        lambda_label = lambda_vals2labels[lambda_val]
        self.sky_table[ self.sky_table['theta']==theta,\
                        self.sky_table['phi']==phi]+=1


    def make_lambda_lookups(self,lambdas):

        self.make_lambda_vals2labels(lambdas)
        self.lambda_labels2vals={v:k for k,v in self.lambda_vals2labels.items()}

    def make_lambda_vals2labels(self,lambdas):
        
        for i, lambdai in enumerate(lambdas):
            self.lambda_vals2labels[lambdai]= 'lambda_%s' %(i)

if __name__=='__main__':
    
    nside=2**10
    npix=12*nside**2 # number of pixels on sphere, npix=12*nside**2, nside $
    ind=np.arange(npix) # index of pointings
    pix_array=np.array( hp.pix2ang(nside, ind)).T 
    theta_in=pix_array[:,0]
    phi_in=pix_array[:,1]

    print len(phi_in), len(theta_in)
    time1=time.time()
    sky_dat1=SkyData()
    sky_dat1.set_pix_lambdas(theta_in, phi_in, np.linspace(.75, 2.4 ,41) )
    
    time3=time.time()
    sky_dat1.increment_hit( theta_in[0], phi_in[0], .75)
    time2=time.time()

    print "Time of Increment: %s" %(time2-time3)
    print "Time of Execution: %s" %(time2-time1)
    print sky_dat1.sky_table
