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
