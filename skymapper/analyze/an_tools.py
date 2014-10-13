def find_missed(self, list_coords, nside, plot_type, theta_lim=pi):
    '''list_coords is a list of tuples [(theta,phi)... ]
       nside is the resolution, of the form 2**n (usually n=8 or n=9)
       plot_type=['deep', 'allsky']
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

