"""
Defines scan strategy 2

"""

def scan_strat2(savename):
    # Polar Cap theta boundary
    theta_cap1=np.arccos(1- 100*(pi/180)**2/(2*pi))

    # FOV Dimensions
    FOV_Dim=(2048*6.2/3600)*(pi/180) # Base Dimension
    FOV_phi=FOV_Dim*2
    FOV_theta=FOV_Dim
    #Nstrip=21 # Number of strips on each band of FOV 
    #Nsteps= np.ceil( (2 * theta_cap1 / (FOV_phi/(Nstrip*2)) + 2*Nstrip)*2) # (Cap diameter)/(width of strip) + steps for lagging band to get across *2 for Nyquist  
        
    # Define sky pointings ( list of tuples (theta,phi,psi) )

    # STRATEGY 2 
    cent_line_dist1= FOV_Dim/2.0
    cent_lin_dist2= (3.0/2)*FOV_Dim

    theta_cap= theta_cap1+ FOV_Dim
    phi=0
    Num_Points=Nsteps

    pointings1 =[]

    for phi in np.linspace(0,2*pi,365)[0:-1]:   
        list1 = gen_strat2(-cent_line_dist, phi, theta_cap, Num_Points)
        list2= gen_strat2(cent_line_dist, phi, theta_cap, Num_Points)
        pointings1 += list1+list2

    # Instantiate SkyMap class (converts pointing to sky pixels seen)
    # NOTE: nside=2^m for m in [0, 1, 2, 4...], npix=12*nside^2

    skymap = SkyMap(nside=2**9,LVF_theta=FOV_theta, LVF_phi=FOV_phi, cap_theta=theta_cap1+3*FOV_Dim, Nstrips=Nstrip, lambda_min1=.75, lambda_min2=1.25) 

    # Make skymap dictionary from defined sky pointings
    for i,tuple_point in enumerate(pointings1):
        print i
        skymap.make_dicts(i, tuple_point)
    
    skymap.save_lambda_dict(savename)
