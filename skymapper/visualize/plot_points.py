"""
Short function for making radial (not deep sky) plots of sky pointings
"""
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np
from numpy import pi, sin
import pandas as pd

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
    scat= ax.scatter(phi_list, rad_list, s=5, edgecolors='none')

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
   
    Dec=pi/2-theta_vals
    RA= phi_vals
    RA[RA>pi]-= 2*pi
    
    vmin=1
    vmax=5
    #vmin=np.min(hits)
    #vmax=np.max(hits)
    c_vals=hits
    cmap=plt.cm.terrain
    cmaplist=[cmap(i) for i in range((cmap.N*1)/8,(cmap.N*6)/8)]
    cmap=cmap.from_list("Cusom cmap", cmaplist, cmap.N)
    bounds=np.arange(vmin-1,vmax+1,1)+.5
    bound_ticks=np.arange(vmin,vmax+1,1)
    norm=mpl.colors.BoundaryNorm(bounds, cmap.N)


    fig= plt.figure()
    ax= plt.subplot(111, projection="mollweide")
    #ax= plt.subplot(111)
    scat= ax.scatter(RA, Dec, s=5, c=c_vals, cmap=cmap,vmin=vmin, vmax=vmax, edgecolors='none')
    ax.set_xticks([-2*pi/3,-pi/3,0,pi/3, 2*pi/3])
    ax.set_yticks([-pi/4,0,pi/4])
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)

    plt.grid(True)
    #plt.title(plot_title + "; Total Hits %s" %(Nhits), y=1.06, color='b')


    ax2=fig.add_axes([.905,.2,.06,.6])
    cbar=mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, 
                      boundaries=bounds, 
                      ticks=bound_ticks)

    #cbar.ax.set_aspect(8)
    cbar.ax.tick_params(labelsize=24)
    #cbar=fig.colorbar(scat, ticks=[10,15,20])
    #cbar=fig.colorbar(scat)

    fig.set_size_inches(12,8)
    plt.savefig(savename+".png" )

def moll_plot2(theta_vals, phi_vals, hits, plot_title, savename):
    """
    :param 
    """
    Nhits= np.sum(hits)
   
    Dec=pi/2-theta_vals
    RA= phi_vals
    RA[RA>pi]-= 2*pi
    
    vmin=np.min(hits)
    vmax=np.max(hits)
    #vmin=np.min(hits)
    #vmax=np.max(hits)
    c_vals=hits
    cmap=plt.cm.Oranges
    cmaplist=[cmap(i) for i in range((cmap.N*1)/3,(cmap.N*8)/8)]
    cmap=cmap.from_list("Cusom cmap", cmaplist, cmap.N)
    bounds=np.arange(vmin-1,vmax+1,1)+.5
    bound_ticks=np.round(np.linspace(vmin,vmax+1,4),0)
    norm=mpl.colors.BoundaryNorm(bounds, cmap.N)


    fig= plt.figure()
    ax= plt.subplot(111, projection="mollweide")
    #ax= plt.subplot(111)
    scat= ax.scatter(RA, Dec, s=5, c=c_vals, cmap=cmap,vmin=vmin, vmax=vmax, edgecolors='none')
    ax.set_xticks([-2*pi/3,-pi/3,0,pi/3, 2*pi/3])
    ax.set_yticks([-pi/4,0,pi/4])
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)

    plt.grid(True)
    #plt.title(plot_title + "; Total Hits %s" %(Nhits), y=1.06, color='b')


    ax2=fig.add_axes([.905,.2,.06,.6])
    cbar=mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, 
                      boundaries=bounds, 
                      ticks=bound_ticks)

    #cbar=mpl.colorbar.ColorbarBase(ax2,cmap=cmap)
    #cbar.ax.set_aspect(8)
    cbar.ax.tick_params(labelsize=24)
    #cbar=fig.colorbar(scat, ticks=[10,15,20])
    #cbar=fig.colorbar(scat)
    
    print ax.get_position(), ax2.get_position()

    pos2=ax2.get_position()
    ax2.set_position([pos2.x0-.02, pos2.y0, pos2.width, pos2.height])

    pos1=ax.get_position()
    ax.set_position([pos1.x0-.02, pos1.y0, pos1.width, pos1.height])

    fig.set_size_inches(12,8)
    plt.savefig(savename+".png" )

    print ax.get_position(), ax2.get_position()

def poll_plot(theta_vals, phi_vals, hits, plot_title, savename):
    """
    :param 
    """
    Nhits= np.sum(hits)
    ang_in = phi_vals   
    rad_in=np.sin(theta_vals)    

    vmin=0
    vmax=180
    c_vals=hits
    cmap=plt.cm.hot
    cmaplist=[cmap(i) for i in range(cmap.N/10,(cmap.N*6)/7)]
    cmap=cmap.from_list("Cusom cmap", cmaplist, cmap.N)

    fig= plt.figure()
    ax= plt.subplot(111, projection="polar")
    scat= ax.scatter(ang_in, rad_in, s=5, c=c_vals, cmap=cmap,vmin=vmin, vmax=vmax, edgecolors='none')

    print ax.get_position()
    ax.set_rgrids(radii=sin(pi/2-np.array([85*pi/180,80*pi/180])),\
        labels=np.around(np.array([85.0,80.0]),2),\
        angle=70, size='large')

    plt.grid(True)
    #ax.set_xticks([-2*pi/3,-pi/3,0,pi/3, 2*pi/3])
    #ax.set_yticks([-pi/4,0,pi/4])
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    #plt.title(plot_title + "; Total Hits %s" %(Nhits), y=1.06, color='b')

    #cbar=fig.colorbar(scat, ticks=[10,15,20])
    cbar=fig.colorbar(scat, pad=.15)
    cbar.ax.set_aspect(8)
    cbar.ax.tick_params(labelsize=20)

    fig.set_size_inches(12,8)
    plt.savefig(savename+".png" )



if __name__=='__main__':
    #moll_plot_points(list_points=[(theta,phi) for theta in np.linspace(0,pi,20) 
    #for phi in np.linspace(0,2*pi,5) ], plot_title="Test", savename='test' )

    moll_plot2(np.linspace(pi/4,pi/2,20), np.linspace(0,2*pi,20), np.array([1,1,1,2,3,4,3,2,1,20,2,3,1,40,4,5,70,80,1,100,4]), "SaveTitle", "CheckMollPlot")
    #poll_plot(np.array([pi/32,3*pi/64, pi/32]), np.array([pi/32,-pi/2, pi/4]), np.array([40.0,80.0,150.0]), "SaveTitle", "CheckPolPlot")
#    arr=np.load("checksums.npy")
#    moll_plot(arr[:,0],arr[:,1], arr[:,3], "SaveTitle", "CheckMollPlot")

#    df=pd.load("testdf_2")
#    group1=df.groupby(level=2)
#    testarr=group1.reset_index().values
#    FOV=3.52*pi/180.0

#    for key in df.index.get_level_values(level=2):
#        arr=testarr[testarr[:,2]==key]
#        arr=arr[(arr[:,1] > pi-FOV) & (arr[:,1] < pi+FOV )]
#        arr=arr[arr[:,3]==0]
#        print arr
#        cmap=np.ones(len(arr[:,3]))
#        cmap[0]*=2
#        moll_plot(arr[:,0],arr[:,1], cmap, "SaveTitle", "CheckMollPlot_%s"%(key))
#        print key
