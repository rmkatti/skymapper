import numpy as np
from numpy import pi
import healpy as hp
import itertools
from collections import Counter
import cPickle as pickle
import time

def find_missed(list_coords, nside, theta_lim=pi):
    '''list_coords is a list of tuples [(theta,phi)... ]
       nside is the resolution, of the form 2**n (usually n=8 or n=9)
       theta_lim (on range [0,pi]) only applicable if plot_type='deep'  '''


    print len( list_coords)
    list_coords=np.around(np.asarray(list_coords),5)
    dtype1= np.dtype( (np.void, list_coords.dtype.itemsize * list_coords.shape[1] ) ) 
    b = np.ascontiguousarray(list_coords).view(dtype1)
    _, idx= np.unique(b, return_index=True )
    list_coords=list_coords[idx]

    #for thet in np.unique(list_coords[:,0]):
    #    for np.unique( list_coords[ list_coords[:,0]==thet ]  )
    idx2 = np.argsort(list_coords[:,0])
    list_coords=list_coords[idx2]
    #print "after list_coords", list_coords[0:15]
        

    npix=12*nside**2 # number of pixels on sphere, npix=12*nside**2, nside = 2^0, 2^1, 2^2 . . .
    ind=np.arange(npix) # index of pointings
    pix_array=np.array( hp.pix2ang(nside, ind)).T # Unrotated sky pixels
    sky_pixels= pix_array[ pix_array[:,0]<= theta_lim ]
    sky_pixels=np.around(sky_pixels, 5)    
    sky_pixels= sky_pixels[ np.argsort(sky_pixels[:,0]) ]
    #print "len internal sky pixels", len(sky_pixels)
        
    out_list= np.empty([1,2])
    #print np.unique(list_coords[:,0])
 

    for thet in np.unique(sky_pixels[:,0]):
        for phi in sky_pixels[ sky_pixels[:,0]==thet][:,1]:

            if phi not in list_coords[ list_coords[:,0]==thet][:,1]:
                out_list=np.append(out_list, np.array([[thet,phi]]), axis=0)

    final_out = out_list[1:]
    print len(final_out)

    return final_out


def lam_dict_to_array(lambda_dict1):
    '''This function converts a dictionary {lambda1:[(theta1_1,phi_1_2)]...}
    to a numpy array with col1 theta, col2 phi, col3 lambda1 hits . . . '''

    list_pix_centers=list(itertools.chain(*lambda_dict1.values()))
    unique_centers=list(set(list_pix_centers))
    
    row_dim = len(list_pix_centers)
    col_dim = 2+len(lambda_dict1.keys())
    out_array=np.zeros([row_dim, col_dim])
    array_len=0
    

    # Generate sparse output array
    for num, lambdai in enumerate(sorted(lambda_dict1.keys())):

        listi=lambda_dict1[lambdai] 
        hits_dict=Counter(listi)
        delta=len( hits_dict.keys() )

        start= array_len
        end=  array_len+delta

        out_array[start:end,:2]= np.asarray( hits_dict.keys() )
        out_array[start:end, num+2]= np.asarray( hits_dict.values() )
        
        array_len=end

    out_array=out_array[:array_len]
    out_array=np.round(out_array,7)
    # Simplify array

    simp_array=np.zeros([len(unique_centers), col_dim+1])

    for i, tupler in enumerate(unique_centers):
        theta= tupler[0]
        phi= tupler[1]

        delta_array= out_array[ (out_array[:,0]==np.round(theta,7) ) & ( out_array[:,1]==np.round(phi,7)) ]
        delta_array= delta_array[:, 2:]
        sum_list=delta_array.sum(axis=0)
        Nhits= np.array([sum_list.sum()])

        if not Nhits>0:
           raise ValueError("Nhits=%s" %(Nhits))
        
        simp_array[i,:] = np.concatenate( (np.asarray(tupler), Nhits, sum_list) ) 

    return simp_array
  

if __name__=='__main__':

    #lambda2={.75:[(0,1),(0,1),(1,2)], .76:[(0,1),(0,1),(3,4),(3,4),(3,4),(4,5),(4,5)], 
    #.77:[(0,1),(1,2),(4,5),(6,7)]}
    time1= time.time()
    lambda2=pickle.load(open("lambda_dict_deep_test","rb"))
    time2=time.time()

    array2=lam_dict_to_array(lambda2)
    np.savetxt('array_file', array2, delimiter=', ' )
    print "Time Elapsed: %s" %(time2-time1)    
