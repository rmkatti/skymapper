def gen_strat2(cent_line_dist, phi, theta_cap, Num_Points):
    """This function generates a list of pointings 
    [(theta_1,phi_1, psi=0),(theta_2,phi_2, psi=0) . . .] for input into the skymapper2 
    program

    cent_line_dist:
    phi:
    theta_cap:
    Num_Points:

    """
 
    if np.round(cent_line_dist,8)==0:
        raise ValueError("np.round(cent_line_dist,8)==0. cent_line_dist=%s" %(cent_lin_dist) )
    rcap = np.sin(theta_cap)

    if rcap <0:
        raise ValueError("rcap must be positive. rcap=%s, theta_cap=%s" %(rcap, theta,cap))

    if np.absolute(cent_line_dist) > rcap:
        raise ValueError("cent_line_dist (=%s) > rcap (=%s)" %(cent_line_dist, rcap))
 
    wmin = np.arcsin(float(cent_line_dist) / rcap) # wmin on [-pi/2,pi/2]

    if wmin >= 0: # Top line (relative to phi=0)
        xrange=np.linspace(float(cent_line_dist)/np.tan(wmin), float(cent_line_dist)/np.tan(pi-wmin), Num_Points)

    elif wmin < 0: # Bottom line (relative to phi=0)
        xrange=np.linspace(float(cent_line_dist)/np.tan(wmin),float(cent_line_dist)/np.tan(-pi-wmin), Num_Points)

    elif type(wmin) != np.float64:
        raise ValueError("wmin not type np.float64. type(wmin) is %s" %(type(wmin)))

    else:
        raise ValueError("wmin invalid np.float64")

    R=np.array([ [np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)] ])
    list_points=[]

    for i, xval in enumerate(xrange):
        y= cent_line_dist 
        x= xval

        if x > rcap:
            raise ValueError("x > rcap. x=%s" %(x))
        
        vec=np.array([[x],[y]]) 
        
        rot_vec = np.dot(R,vec)
        
        x_rot = rot_vec[0].item()
        y_rot = rot_vec[1].item()
        
        r=(x_rot**2 + y_rot**2)**.5
        theta_out=np.arcsin(r)
      
        if not 0 < theta_out < pi/2:
            raise ValueError("theta_out not between 0 and pi/2. theta_out=%s" %(theta_out))

        phi_out=np.arctan2(y_rot,x_rot)

        if -pi < phi_out < 0:
            phi_out += 2*pi

        if not 0 <= phi_out <= 2*pi:
            raise ValueError("phi_out=%s out of range [0, 2*pi]" %(phi_out))
 
        list_points.append((theta_out, phi_out, -phi_out+phi-pi/2))

    return list_points

