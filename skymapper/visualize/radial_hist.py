"""
These functions take a lambda_dict, and minimum and maximum lambda values and return a
histogram with radial bins and frequency the number of hits in that wavelength range.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
#from numpy import pi, cos, sin
from numpy import pi
import collections as coll
import cPickle as pickle
from collections import Counter
import pandas as pd

def lambda_radial_histogram(lambda_dict1, lambda_min, lambda_max, savename):
    """This function takes as argument a dictionary 
    lambda1:[(theta1,phi1,...)]. It makes a histogram of hits, where
    each bin is in equal-area radial slice.

    :M Area (in steradians) of each radial slice
    :theta_min (on range [0,pi]) initial value of theta
    :theta_max (on range [0,pi]) final value of theta
    """

    print "Doing Keys"
    keys = np.asarray(lambda_dict1.keys())
    keys= keys[(keys<lambda_max) & (keys>=lambda_min)]
        
    print "Making Data"
    for i,key in enumerate(keys):
        print i
        if i==0:
            data= np.asarray(lambda_dict1[key])[:,0]
        else:
            data=np.append( data, np.asarray(lambda_dict1[key])[:,0], axis=0)

    data=np.around(data, decimals=10)
    data1= Counter(data)
    print "data1 created"
    
    thetas, freq = zip( *sorted(data1.items()) )
    thetas=np.asarray(thetas)
    dec= np.around(90-(180/pi)*thetas,2)

    freq=np.asarray(freq)
    num_sum= freq.sum()
    #freq=freq/(2*pi*np.sin(thetas)) # Uncomment if want a 2*pi*r normalization
    thet_dist= num_sum*freq/freq.sum()
    Nhits=thet_dist.sum()
        
    print "Making Plot"
    fig=plt.figure()
    ax=plt.subplot(111)
    bar=ax.bar(thetas, thet_dist , width=.001)
    #bar=ax.scatter(thetas, thet_dist)
        
    strt= len(thetas)/40
    incr = len(thetas)/5
        
    plt.xticks([thetas[0],thetas[len(thetas)/4], thetas[len(thetas)/2], thetas[(len(thetas)*3)/4], thetas[-1]], [dec[0],dec[len(dec)/4], dec[len(dec)/2],dec[(len(dec)*3)/4], dec[-1]] )

    #fig.suptitle( "Number Density Distribution; lambda [%.2fum,%.2fum); Total Hits %s" %(lambda_min, lambda_max, Nhits) )
    fig.suptitle( "Radial Hits Histogram; lambda [%.2fum,%.2fum); Total Hits %s" %(lambda_min, lambda_max, Nhits) )
    plt.xlabel("Dec")
    #plt.ylabel("Number Density")
    plt.ylabel("Number of Hits per Radial Bin")
    fig.set_size_inches(9.0,6.0)

    savename_out="%s_hist_%.2f_%.2f.png" %(savename,lambda_min, lambda_max)
    
    plt.savefig(savename_out, dpi=500)

    #plt.show()
    "Done"

def radial_hist_numpy_arrays(array_bin, array_count):
    
    df=pd.DataFrame({'bins': array_bin , 'counts': array_count})
    #out=df.groupby('bins')['counts'].sum()
    out=df.groupby('bins')['counts'].mean()
    out_vals=out.reset_index().values
    
    bin_vals=np.sin( out_vals[:,0] )
    count_vals=out_vals[:,1]
    return bin_vals, count_vals

def make_radial_hist_figs(thetas, thet_dist, savename):
    Nhits = np.sum(thet_dist)
    dec= np.around(90-(180/pi)*thetas,2)


    fig=plt.figure()
    ax=plt.subplot(111)
    bar=ax.bar(thetas, thet_dist , width=.001)
    #bar=ax.scatter(thetas, thet_dist)
        
    strt= len(thetas)/40
    incr = len(thetas)/5
        
    plt.xticks([thetas[0],thetas[len(thetas)/4], thetas[len(thetas)/2], thetas[(len(thetas)*3)/4], thetas[-1]], [dec[0],dec[len(dec)/4], dec[len(dec)/2],dec[(len(dec)*3)/4], dec[-1]] )

    #fig.suptitle( "Number Density Distribution; lambda [%.2fum,%.2fum); Total Hits %s" %(lambda_min, lambda_max, Nhits) )
    fig.suptitle( "Least Radial Hits Histogram; Total Hits %s" %(Nhits) )
    plt.xlabel("Dec")
    #plt.ylabel("Number Density")
    plt.ylabel("Number of Hits per Radial Bin")
    fig.set_size_inches(9.0,6.0)

    savename_out="%s_least_hist.png" %(savename)    
    plt.savefig(savename_out, dpi=500)

def make_least_radial_hist(name):

    array1=np.load(name)
    thetas=array1[:,0]
    min_hits = np.amin(array1[:,3:], axis=1)    
    bin_vals1, count_vals1 =  radial_hist_numpy_arrays(thetas, min_hits)
    make_radial_hist_figs(bin_vals1, count_vals1, 'MEAN_%s' %(name))

if __name__=='__main__':

    make_least_radial_hist('array_test_FOM.npy')
