"""
Short function for making radial (not deep sky) plots of sky pointings
"""
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import numpy as np
from numpy import pi

def rad_plot_points(list_points, savename):
    """
    :param list_points, list of tuples of sky pointings 
        e.g. [(theta1,phi1,ax1), (theta2, phi2, ax2)...] 
    """

    theta_vals, phi_vals = zip(*list_points)
    rad_list = [ theta for theta in theta_vals ]
    phi_list = [ phi for phi in phi_vals]

    fig= plt.figure()
    ax= plt.subplot(111, polar=True)
    scat= ax.scatter(phi_list, rad_list, s=10, edgecolors='none')

    plt.savefig(savename+".png" )

def moll_plot_points(list_points, plot_title, savename):
    """
    :param list_points, list of tuples of sky pointings 
        e.g. [(theta1,phi1,ax1), (theta2, phi2, ax2)...] 
        theta on [0,2*pi], phi on 0,2*pi
    """

    Nhits= len(list_points)
    theta_vals, phi_vals = zip(*list_points)

    Dec=pi/2-np.asarray(theta_vals)
    RA= np.asarray(phi_vals)
    RA[RA>pi]-= 2*pi    

    fig= plt.figure()
    ax= plt.subplot(111, projection="mollweide")
    scat= ax.scatter(RA, Dec, s=5)
    plt.grid(True)
    plt.title(plot_title + "; Total Hits %s" %(Nhits), y=1.06, color='b')
    fig.set_size_inches(20.0,10.0)

    plt.savefig(savename+".png" )

def moll_plot(theta_vals, phi_vals, hits, plot_title, savename):
    """
    :param 
    """
    Nhits= np.sum(hits)
   
    Dec=pi/2-np.asarray(theta_vals)
    RA= phi_vals
    RA[RA>=pi]-= 2*pi
    
    c_vals=hits
    cmap=plt.cm.jet

    fig= plt.figure()
    ax= plt.subplot(111, projection="mollweide")
    scat= ax.scatter(RA, Dec, s=10, c=c_vals, cmap=cmap, edgecolors='none')

    plt.grid(True)
    plt.title(plot_title + "; Total Hits %s" %(Nhits), y=1.06, color='b')

    fig.colorbar(scat)
    fig.set_size_inches(20.0,10.0)
    plt.savefig(savename+".png" )



if __name__=='__main__':
    #moll_plot_points(list_points=[(theta,phi) for theta in np.linspace(0,pi,20) 
    #for phi in np.linspace(0,2*pi,5) ], plot_title="Test", savename='test' )

    moll_plot(np.array([pi/4,3*pi/4]), np.array([pi/2,-pi/2]), np.array([10.0,20.0]), "SaveTitle", "CheckMollPlot")
    
