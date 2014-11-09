import numpy as np
from numpy import pi
import healpy as hp
import itertools
from collections import Counter
import cPickle as pickle
import time
import scipy.stats as scistat

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

def mean_colormap(array1):
    '''Outputs a useful colormap based on mean of wavelengths'''

    arr1=array1[:,3:]
    c=np.mean(arr1, axis=1)
    return array1[:,0], array1[:,1], c


def std_colormap(array1):
    '''Outputs a useful colormap based on std of wavelengths'''

    arr1=array1[:,3:]
    c=np.std(arr1, axis=1)
    return array1[:,0], array1[:,1], c

def FOM_2(array1):

    Nhits = np.sum(array1[:,2])
    min_sum = np.sum( np.amin(array1[:,3:], axis=1) )
    Num_channels = len(array1[0,3:])
    Eff= Num_channels*min_sum / np.float(Nhits)

    Area_unnormed= np.sum( ((180/pi)*array1[:,0])**2 * np.amin(array1[:,3:], axis=1) )
    Area_normed= Area_unnormed / np.float(min_sum)
    #Area_norm_degree=Area_normed*(180/pi)**2

    n_dense_degree = Eff*(np.float(Nhits)/Num_channels)/Area_normed

    FOM_2=Eff/np.sqrt(Area_normed)

    return (FOM_2, n_dense_degree, Eff, Area_unnormed,Area_normed, min_sum, Nhits, Num_channels)


def histogram_pixel(row_id, array1):

    lambdas=array1[row_id][3:]
    ret_mat=scistat.itemfreq(lambdas)

    return ret_mat[:,0], ret_mat[:,1]



def lam_dict_to_array(lambda_dict1):
    '''This function converts a dictionary {lambda1:[(theta1_1,phi_1_2)]...}
    to a numpy array with col1 theta, col2 phi, col3 lambda1 hits . . . '''

    list_pix_centers=list(itertools.chain(*lambda_dict1.values()))
    unique_centers=list(set(list_pix_centers))
    
    row_dim = len(list_pix_centers)
    col_dim = 2+len(lambda_dict1.keys())
    out_array=np.zeros([row_dim, col_dim], dtype=np.float32)
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

        timei_1= time.time()
        
    
    out_array=out_array[:array_len]
    out_array=np.round(out_array,7)
    
    
    # Simplify array
    time1=time.time()

    ind_in=out_array[:,:2]
    join_row = np.ascontiguousarray(ind_in).view( np.dtype( (np.void,\
             ind_in.dtype.itemsize * ind_in.shape[1] )))
    _, unique_rows, indices= np.unique(join_row, return_index=True, return_inverse=True)

    time2=time.time()
    print "Time of array blocks ", time2-time1

    simp_array=np.zeros([len(unique_rows), col_dim+1])

    print len(set(indices))   
    timei=time.time()

    for i, val in enumerate(set(indices)):

        theta_phi=out_array[indices==val][0,0:2]
        summed_lambda=np.sum(out_array[indices==val][:,2:], axis=0)
        N_pix = np.array([sum(summed_lambda)])
        simp_array[i]=np.concatenate((theta_phi, N_pix, summed_lambda))
           
        if i%1000==0:
            time_i1=time.time()
            print i, time_i1-timei
            timei=time.time()

 #   for i, val in enumerate(unique_rows):
 #       time1=time.time()

        
        #theta= tupler[0]
        #phi= tupler[1]

        #delta_array= out_array[ (out_array[:,0]==np.round(theta,7) ) & ( out_array[:,1]==np.round(phi,7)) ]
        #delta_array= delta_array[:, 2:]
        #sum_list=delta_array.sum(axis=0)
        #Nhits= np.array([sum_list.sum()])

        #if not Nhits>0:
        #   raise ValueError("Nhits=%s" %(Nhits))
        
        #simp_array[i,:] = np.concatenate( (np.asarray(tupler), Nhits, sum_list) ) 
        #time2=time.time()
        #print time2-time1

    return simp_array

def save_converted_array(array1, array_savename ):

    np.save(array_savename, array1)  


if __name__=='__main__':

    #lambda2={.75:[(0,1),(0,1),(1,2)], .76:[(0,1),(0,1),(3,4),(3,4),(3,4),(4,5),(4,5)], 
    #.77:[(0,1),(1,2),(4,5),(6,7)]}

    #time5= time.time()
    #lambda2=pickle.load(open("lambda_dict_deep_test","rb"))
    #time6=time.time()
    #print "Open file: %s" %(time6-time5)    

    #array2=lam_dict_to_array(lambda2)
    #np.savetxt('array_file', array2, delimiter=', ' )
    #time7=time.time()
    #print "Full Program Time: ", time7-time5

    array_savename='test_array'
    dict1 = {1:[(pi/8,pi/2),(pi/8,pi/2),(pi/8,pi/2),(pi/8,pi/4),(pi/8,pi/8)], 2: [(pi/8,pi/2),(pi/8,pi/4),(pi/8,pi/4),(pi/8,pi/3)], 3:[(pi/8,pi/2),(pi/8,pi/2),(pi/8,pi/4),(pi/5,pi/3)]}
    array1=lam_dict_to_array(dict1)
    save_converted_array(array1, array_savename )
    print array1
    out_tuple = FOM_2(array1)

    print "out_tuple", out_tuple
