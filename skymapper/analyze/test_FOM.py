from skymapper.gen_maps.lambda_set_2 import *
import healpy as hp
import numpy as np
import cPickle as pickle
from numpy import pi

def gen_test_pixels(nside=2**9, theta_max=5.6419*(pi/180.0), keyword1='list'):
    '''Keyword ['list', 'array']'''

    npix=12*nside**2 # number of pixels on sphere, npix=12*nside**2, nside = 2^0, 2^1, 2^2 . $
    ind=np.arange(npix) # index of pointings
    pix_array=np.array( hp.pix2ang(nside, ind)).T # Unrotated sky pixels

    sky_pixels= pix_array[ pix_array[:,0]<= theta_max ]
    
    if keyword1== 'list':
        sky_pixels=map(tuple, sky_pixels)
          
    return sky_pixels

def gen_lambda_test_dict(redund=116):

    lambda_band1= gen_lambda(lambda_min=.75, lambda_max=1.32, R=41.95625926211772)
    lambda_band2= gen_lambda(lambda_min=1.32, lambda_max=2.34, R=41.95625926211772)

    sky_pix=gen_test_pixels()
    sky_pix_add=sky_pix*redund
    lambda_dict={}
    lambda_list=lambda_band1[:-1]+lambda_band2[:-1]

    for i, lambdai in enumerate(lambda_list):
        print lambdai
        lambda_dict[lambdai]= sky_pix_add
        print len(lambda_dict.values()[i])

    return lambda_dict


if __name__=='__main__':

    lambda_dict1 = gen_lambda_test_dict(redund=116)
    print "Dict Made", 

    for list1 in lambda_dict1.values():
        print len(list1)    

    pickle.dump( lambda_dict1, open( "lambda_dict_test_FOM", "wb" ) )

    #for list1 in lambda_dict1.values():
    #    print len(list1)
