'''
This class generates a dictionary of sky pixel coverage at each wavelength
for a rectangular linear variable filter with two wavelength bands placed 
symmetrically about the longer dimension. 

Future Work: Generalization to arbitrary field of view

Initialization defines the field of view (FOV) dimensions and wavelength 
steps across the FOV. In our case, the FOV is a rectangular linear variable 
filter (LVF), parametrized by an azimuthal range and a polar range.

Input to the make_dicts() method is a scan strategy denoting the pointing 
directions of the FOV. It is a list of tuples 
[(theta1,phi1,ax1), (theta2,phi2,ax2)... ] where thetas are the polar 
angle of the FOV center on [0,pi], phis are the azimuthal angle of the 
FOV center on [0,2*pi], and the ax's are axial angle about the axis defined from 
the origin through the FOV center

Output is a dictionary with wavelengths as keys and a list of 
sky pixel centers (theta,phi) viewed at that wavelength.
'''

import numpy as np
import healpy as hp
from numpy import pi, cos, sin
import cPickle as pickle
from skymapper.gen_maps.lambda_set_2 import *
import time

class SkyMap(object):
    
    def __init__(self, nside,LVF_theta, LVF_phi, cap_theta):
    
        """We initialize the FOV dimension.

        :param nside is a healpix parameter for discretization of the sky, nside=2**n
        for n=0,1,2....

        :param LVF_theta, defined for LVF center located at (theta=pi/2, phi=0). Defines
        theta range (height) of LVF

        :param LVF_phi, defined for LVF center located at (theta=pi/2, phi=0). Defines 
        phi range (width) of LVF

        :param cap_theta, discretizes sky on theta range [0, cap_theta]. Set cap_theta=pi for allsky    scan

        """

        # Define sky pixels
        npix=12*nside**2 # number of pixels on sphere, npix=12*nside**2, nside = 2^0, 2^1, 2^2 . . .
        ind=np.arange(npix) # index of pointings
        pix_array=np.array( hp.pix2ang(nside, ind)).T # Unrotated sky pixels

        self.sky_pixels= pix_array[ pix_array[:,0]<= cap_theta ]
       
        if self.sky_pixels == []:
            raise TypeError("sky_pixels empty")
            #theta_vals on [0,pi], phi_vals on [0,2*pi]

        # LVF theta and phi bounds
        self.LVF_theta_dim= LVF_theta
        self.LVF_phi_dim= LVF_phi

        self.theta_low=pi/2-LVF_theta/2
        self.theta_hi=pi/2+LVF_theta/2
        self.phi_low=2*pi-LVF_phi/2
        self.phi_hi=LVF_phi/2

        # rotated coordinates and dictionaries to be defined by make_dicts
        self.rot_sky_pixels=[]
    	self.lambda_dict={} # Key: Values:
       
    def make_dicts(self, pointID, pointing):
        '''Takes a pointID (usually a integer) and a single pointing (tuple of 
        pointing angles (theta,phi,psi)) and updates the self.* dictionaries 
        with key pointID (usually an integer) and value a list of skypixels 
        seen
        e.g. {pointID1:[ (theta0, phi0), (theta1, phi1)...], pointID2:...} '''
              
        theta, phi, psi=pointing
       
        # R1 is the matrix rotating the healpix pixel centers to the frame
        # in which the pointing center (thetac,phic) is at 
        # (x=1,y=0,z=0)=(thetac_new=pi/2, phic_new=0), R1inv is the inverse 
        #matrix

        
        cutoff_dim = max(self.LVF_theta_dim, self.LVF_phi_dim)
        upper_theta= theta+1.5*cutoff_dim
        lower_theta= theta-1.5*cutoff_dim

        sky_pixels_in = self.sky_pixels[ ( self.sky_pixels[:,0]<upper_theta) & (self.sky_pixels[:,0]>lower_theta) ]
     
        if  (30.0*pi/180 < theta < 150.0*pi/180.0) & (pi/4< phi < 7*pi/4):
            upper_phi= phi + 1.5*cutoff_dim
            lower_phi= phi - 1.5*cutoff_dim
            sky_pixels_in = self.sky_pixels[ (self.sky_pixels[:,1] < upper_phi) & (self.sky_pixels[:,1] > lower_phi)  ]

        R1, R1inv= self.rot_matrix(theta,phi,psi)
        
        self.rot_sky_pixels=np.array(self.rotate(sky_pixels_in, R1)) # Rotated sky pixels
        time2=time.time()
        

        # Make dictionary of rotated pixel pointings. For a given theta, 
        # gives the list of phi values associated with that theta

        skypix_list= np.array([]) # skypix_list[theta]=[phi1,phi2...] 
        
        # Remove thetas outside of bounds
        self.rot_sky_pixels= self.rot_sky_pixels[ (self.theta_low < self.rot_sky_pixels[:,0]) & (self.rot_sky_pixels[:,0] <= self.theta_hi)] 

        vec1 =self.rot_sky_pixels[ (0 <= self.rot_sky_pixels[:,1]) & ( self.rot_sky_pixels[:,1] <= self.phi_hi)] 
        vec2 =self.rot_sky_pixels[ (self.phi_low <= self.rot_sky_pixels[:,1]) & ( self.rot_sky_pixels[:,1] < 2*pi)] 
    
        self.rot_sky_pixels = np.append(vec1,vec2, axis=0)
       
        # Define lambda and phi edges
        lambda_band1= gen_lambda(lambda_min=.75, lambda_max=1.32, R=41.95625926211772)
        phi_band1 = np.linspace(self.phi_low, 2*pi, 25)
         
        lambda_band2= gen_lambda(lambda_min=1.32, lambda_max=2.34, R=41.95625926211772)
        phi_band2=np.linspace(0,self.phi_hi, 25)
     
        for i, lambdai in enumerate(lambda_band1[:-1]):
            phi_mini = phi_band1[i]  
            phi_maxi = phi_band1[i+1]

            datain = self.rot_sky_pixels[(self.rot_sky_pixels[:,1] < phi_maxi) & (self.rot_sky_pixels[:,1] >= phi_mini)]
            if np.size(datain)==0:
                list_list=[]
            else:
                list_list=self.rotate(datain, R1inv).tolist()
            self.lambda_dict.setdefault(lambdai,[]).extend( map(tuple,list_list) ) 


       # lam/del_lam=R
       # lam/R = del_lam
       # lambda2=lambda1+lambda1/R
       # lambda3=lambda2+lambda2/R
       #        =lambda1+lambda1/R + (lambda1+lambda1/R)/R  
  
        for i, lambdai in enumerate(lambda_band2[:-1]):
            phi_mini = phi_band2[i]
            phi_maxi = phi_band2[i+1]       

            datain = self.rot_sky_pixels[(self.rot_sky_pixels[:,1] < phi_maxi) & (self.rot_sky_pixels[:,1]>= phi_mini)]
     	    if np.size(datain)==0:
       	       	list_list=[]
       	    else:
      	       	list_list=self.rotate(datain, R1inv).tolist()
            self.lambda_dict.setdefault(lambdai,[]).extend(  map(tuple, list_list) )
                
        # Check Values and add wavelenghth value to lambda_list
             
    def save_lambda_dict(self, name_mod):
        pickle.dump(self.lambda_dict, open("lambda_dict_%s" % name_mod,'w'))
  
    def rotate(self, data, rot_mat):
        '''Input polar (theta), azimuthal (psi), axial (psi) angles. Outputs rotated coordinates '''
        data_rot=np.empty_like(data)
        data=np.array(data)
        vec_i=np.empty([data.shape[0],3])

        vec_i[:,0]= np.sin(data[:,0])*np.cos(data[:,1])
        vec_i[:,1]= np.sin(data[:,0])*np.sin(data[:,1])
        vec_i[:,2]= np.cos(data[:,0])

        pixvec_r=np.inner(rot_mat,vec_i).T

        if pixvec_r.shape != vec_i.shape:
            raise TypeError()

        data_rot[:,0] = np.arccos( pixvec_r[:,2] ) 
        data_rot[:,1] = np.arctan2(pixvec_r[:,1], pixvec_r[:,0])
        data_rot[ data_rot[:,1]< 0 ]+= [0,2*pi]
        
        #if np.round(theta,9)==0.0 or np.round(theta,9)==np.round(pi,9):
        #    return theta,0.0
        if np.any(data_rot[:,0]<0):
            raise ValueError

        return data_rot        

   
    def rot_matrix( self, theta, phi, psi):
        '''Rotates coordinate system such that center FOV at (1,0,0), 
        (i.e. theta=pi/2, phi=0 )and FOV lies along equator (axial=0) '''

        azrot= -phi
        polrot=pi/2-theta
        axial=-psi        
        
        R=np.dot(self.psi_mat(axial), np.dot(self.theta_mat(polrot), self.phi_mat(azrot))) # Matrix multiplication psi_mat*theta_mat*phi_mat
        Rinv=np.dot(self.phi_mat(-azrot), np.dot( self.theta_mat(-polrot),self.psi_mat(-axial) ))
	
        return R, Rinv
  
    def phi_mat(self, azrot):
        '''azimuthal rotation matrix (along z-axis)'''
        return np.array([[cos(azrot), -sin(azrot), 0],[sin(azrot), cos(azrot), 0],[0, 0, 1]])

    def theta_mat(self, polrot):
        '''polar rotation matrix (along +y-axis)'''
        return np.array([[cos(polrot), 0, sin(polrot)],[0, 1, 0],[-sin(polrot), 0, cos(polrot)]])

    def psi_mat(self, axial):
        return np.array([[1,0,0],[0,cos(axial),-sin(axial)],[0,sin(axial),cos(axial)]])

    def sphere2cart(self, theta,phi,r=1):
        """Returns x, y, z. Requires numpy as np. Demand theta on [0,pi] and
        phi on [0,2*pi)"""
        if ( np.trunc(theta*10**9) > pi*10**9 or theta <0.0):
            raise ValueError('theta>pi or theta<0. theta=%s' %theta)
        if (phi<0.0 or np.trunc(phi*10**9)>=2*pi*10**9 ):
            raise ValueError('phi<0 or phi>=2*pi. phi=%s' % phi)

        x=r*np.sin(theta)*np.cos(phi)
        y=r*np.sin(theta)*np.sin(phi)
        z=r*np.cos(theta)
        return x,y,z

    def cart2sphere(self,x, y, z):
        """Returns theta [0,pi], phi [0,2*pi), requires numpy as np"""
     
        if np.round((x**2+y**2+z**2)**.5,9)!=1:
            raise ValueError, 'x,y,z not normalized to 1' 
        theta=np.arccos(z)
        phi=np.arctan2(y,x)

        if np.round(theta,9)==0.0 or np.round(theta,9)==np.round(pi,9):
            return theta,0.0
        else:
            if phi < 0:
                phi += 2*pi
            return theta,phi 


