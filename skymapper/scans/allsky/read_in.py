import numpy as np
from numpy import pi


"Script to read in allsky pointings from a particular file"

def read_in_allsky(file):
    ''' RA on [-180,180], dec on [90,-90], theta on [0,pi], phi on [0,2*pi) '''

    f = open(file, 'r')
    pointings_list=[]

    for line in f:
        RAi, deci= line.split()
        RAi=float(RAi)
        deci=float(deci)
        
        if RAi <0:
            RAi+=360.0

        phi= RAi*pi/180.0
        theta= pi/2.0- deci*pi/180.0
        pointings_list.append((theta,phi,0))
    return pointings_list

def read_in_date(pointing_file):
    ''' Loads a file with col1 day, col2 RA, col3 dec. Outputs a 4-col numpy 
        array: col1 day, col2 theta, col3 phi, col4 az=0.

	Convention:
        RA on 90,-90 
	Dec on 180,-180 
	theta on [0,pi] 
        phi on [0,2*pi]
	'''
    pointings1 = np.loadtxt(pointing_file, dtype=float)
    pointings1 = np.append(pointings1,np.zeros((pointings1.shape[0],1)),1)
    pointings1 = pointings1[:,[0,2,1,3]]    
    
    pointings1[:,2] = np.mod( pointings1[:,2] + 30, 360) - 180.0

    #pointings1=pointings1[ np.absolute(pointings1[:,2])<5 ]

    # Set theta
    pointings1[:,1:3]*=pi/180.0
    pointings1[:,1]*=-1
    pointings1[:,1]+=pi/2.0
    pointings1[ pointings1[:,2]<0, 2]+=2*pi

    return pointings1
 
    #Set phi

