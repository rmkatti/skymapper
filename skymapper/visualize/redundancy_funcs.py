import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import cPickle as pickle
import numpy as np
from numpy import pi, sin
import os
import collections as coll
from skymapper.analyze.an_tools import std_colormap, mean_colormap, histogram_pixel
import time
import pandas as pd


def redu_data(lambda_dict, lambda_min, lambda_max):
    """This method makes a polar plot of the redundancy between two input lambda. Input
       lambda dictionary, lambda_min, lambda_max
        
    plot_type=['deep','allsky']
    """
    redu_list=[] 
    key_list = np.array(lambda_dict.keys())
    key_list= key_list[ (lambda_max > key_list) & (key_list>= lambda_min)]
 
    for key in key_list:
        redu_list+= [ ( round(tupler[0],7) , round(tupler[1],7) ) for tupler in lambda_dict[key] ]
            

    redu_dict=coll.Counter(redu_list) # {(theta1,phi1):#, (theta2,phi2):#...}
    redu_mat=np.asarray(redu_dict.keys())
      
    return redu_mat, redu_dict
          
def redu_deepsky(ax, redu_mat, redu_dict, radius_line=5.44*pi/180):

    '''Plot deepsky redundancy map. Input axis should be type polar.'''
     # Define colormap
    cmap = plt.cm.jet
    Nhits= sum(redu_dict.values())       

        # Plot data
    phi_list= redu_mat[:,1]
    rad_list= np.sin(redu_mat[:,0]) 
    scat= ax.scatter(phi_list, rad_list, s=10, c=redu_dict.values(),\
                    cmap=cmap, edgecolors='none')

        # Set and annotate reference radial line
    phi_rad_plot= np.arange(0,2*pi,.01)
    rad_plot = [sin(radius_line)]*len(phi_rad_plot)
    rad_plotter = ax.plot(phi_rad_plot , rad_plot, color='m', linewidth=1)
    #ax.annotate('dec=%.2f$^\circ$'%(90-radius_line*180/pi), xy=(-pi/2,sin(radius_line)), xytext=(0.4, 0.2), textcoords='figure fraction', arrowprops=dict(facecolor='green',
    #     shrink=.05),bbox=dict(facecolor='blue',alpha=.3) )
    ax.set_rgrids(radii=[ sin(theta) for theta in np.linspace(pi/64,pi/16,3)],labels=90-np.linspace(pi/64,pi/16,3)*180/pi, angle=80, color='DarkOrange',size='medium')
    return scat, Nhits       

def least_deepsky(ax, full_arr,  radius_line=5*pi/180):

    '''Color each pixel by its least hit per wavelength over all wavelengths. 
       Input axis should be type polar.'''

     # Define colormap
    cmap = plt.cm.jet
    #Nhits= sum(redu_dict.values())       

    # To plot only those values with min val>0

    # Only min vals greater than 0 data
    c_vals = np.amin(full_arr[:,3:], axis=1) 
    full_arr= full_arr[ c_vals>0, :]
    c_vals=c_vals[c_vals>0]

    phi_list= full_arr[:,1]
    rad_list= np.sin(full_arr[:,0]) 
    
    if full_arr.size==0:
        print "No min values greater than 0"
        return 

    scat= ax.scatter(phi_list, rad_list, s=15, c=c_vals, cmap=cmap, \
          edgecolors='none')

        # Set and annotate reference radial line
    phi_rad_plot= np.arange(0,2*pi,.01)
    rad_plot = [sin(radius_line)]*len(phi_rad_plot)
    rad_plotter = ax.plot(phi_rad_plot , rad_plot, color='m', linewidth=1)
    #ax.annotate('dec=%.2f$^\circ$'%(90-radius_line*180/pi), xy=(-pi/2,sin(radius_line)), xytext=(0.4, 0.2), textcoords='figure fraction', arrowprops=dict(facecolor='green',
    #     shrink=.05),bbox=dict(facecolor='blue',alpha=.3) )
    ax.set_rgrids(radii=[ sin(theta) for theta in np.linspace(pi/64,pi/16,3)],labels=90-np.linspace(pi/64,pi/16,3)*180/pi, angle=80, color='DarkOrange',size='medium')
    return scat       

def redu_allsky(ax, redu_mat, redu_dict):
    '''Plot all-sky redundancy. ax should be given as a mollweide projection'''
            
    Dec=pi/2-redu_mat[:,0]
    RA = redu_mat[:,1]
    RA[RA>pi]-=2*pi
       
    #ax=plt.subplot(111, projection="mollweide")
    cmap = plt.cm.jet
        
    scat= ax.scatter(RA, Dec, s=5, c=redu_dict.values(),\
        cmap=cmap, edgecolors='none')
   
    Nhits= sum(redu_dict.values())       
  
    ax.grid(True)

    return scat, Nhits

    #plt.title(plot_title + "; Total Hits %s" %(Nhits), y=1.06, color='b')
    #cb=fig.colorbar(scat) # Add colorbar
    #cb.set_label("# of Hits")
    #self.fig.set_size_inches(20.0,10.0)


def ax_pix_histogram(ax, array1, row_id):

    print array1[row_id][0:2]
    vals, freqs = histogram_pixel(row_id, array1)
    
    bars = ax.bar(vals, freqs)

    return bars

def plot_hist(array_name, row_id, savename, title):
 
    fig= plt.figure()
    ax = fig.add_subplot(111)

    array2=np.load(array_name)

    ax_pix_histogram(ax, array2, row_id )

    ax.set_xlabel("Number of Hits Per Wavelength")
    ax.set_ylabel("Frequency")
    fig.set_size_inches(15,10)
    fig.suptitle(title)

    plt.savefig(savename+".png" )  

def array_mean_std_plot(array_name, savedir):

    array_obj=np.load(array_name)
    
    thetas, phis, c_vals= std_colormap(array_obj)
    plot_array_maps(thetas, phis, c_vals, 'std_plot_%s' %(array_name), 'Std Plot of %s' %(array_name), savedir)
    
    theta1, phi1, c_val1 = mean_colormap(array_obj)
    plot_array_maps(theta1, phi1, c_val1, 'mean_plot_%s' %(array_name), 'Mean Plot of %s' %(array_name), savedir )
    
    c_val2 = np.amin(array_obj[:,3:], axis=1) 
    array3= array_obj[c_val2>0]
    c_val2=c_val2[ c_val2>0 ]
    theta2= array3[:,0]
    phi2= array3[:,1]
    print c_val2[c_val2>0].size

    plot_array_maps(theta2, phi2, c_val2, 'least_plot_%s' %(array_name), 'Least Hits Plot of %s' %(array_name), savedir )


def plot_array_maps(theta_vals, phi_vals, c_vals, savename, title, savedir):
    """
    :param list_points, list of tuples of sky pointings
        e.g. [(theta1,phi1,ax1), (theta2, phi2, ax2)...]
    """
   
    cmap=plt.cm.jet

    rad_list = [ theta for theta in theta_vals ]
    phi_list = [ phi for phi in phi_vals]

    fig= plt.figure()
    ax= plt.subplot(111, polar=True)

    if c_vals[c_vals>0].size==0 :
        print "No min values greater than 0"
                
    else:
        print len(phi_list), len(c_vals)
        scat= ax.scatter(phi_list, rad_list,c=c_vals,cmap=cmap, s=35, edgecolors='none')
        print "Run"
        fig.colorbar(scat)
 

    radius_line=5.644*pi/180.0
    phi_rad_plot= np.arange(0,2*pi,.01)
    rad_plot = [sin(radius_line)]*len(phi_rad_plot)
    rad_plotter = ax.plot(phi_rad_plot , rad_plot, color='m', linewidth=1)

    #ax.annotate('dec=%.2f$^\circ$'%(90-radius_line*180/pi), xy=(-pi/2,sin(radius_line)), xytext=(0.4, 0.2), textcoords='figure fraction', arrowprops=dict(facecolor='green',
    #     shrink=.05),bbox=dict(facecolor='blue',alpha=.3) )

    ax.set_rgrids(radii=[ sin(theta) for theta in np.linspace(pi/64,pi/16,3)],labels=90-np.linspace(pi/64,pi/16,3)*180/pi, angle=80, color='DarkOrange',size='medium')

    fig.set_size_inches(20,15)
    fig.suptitle(title)

    plt.savefig(savedir+savename+".png", dpi=150)

def subplot_proposal1(f, ax):
    """Implements specs for the subplot proposal1. Input 3x4 subplot fig and axes handles"""

    f.set_size_inches(20,10)
    ylevel=.3
    f.text(.18, ylevel, '3 Months', fontsize=20)
    f.text(.36, ylevel, '6 Months', fontsize=20)
    f.text(.54, ylevel, '9 Months', fontsize=20)
    f.text(.72, ylevel, '1 Year', fontsize=20)

    f.suptitle('All Sky Survey', fontsize=25)
    f.tight_layout()
    f.subplots_adjust(wspace=.075, hspace=-.4)

def proposal_deepsky_specs(f, ax):
    """Implements specs for the subplot proposal1. Input 3x4 subplot fig 
    and axes handles"""

    f.set_size_inches(20,15)
    ylevel=.08
    f.text(.11, ylevel, '3 Months', fontsize=30)
    f.text(.37, ylevel, '6 Months', fontsize=30)
    f.text(.58, ylevel, '9 Months', fontsize=30)
    f.text(.86, ylevel, '1 Year', fontsize=30)

    f.suptitle('Deep Sky Survey', fontsize=35)
    f.tight_layout()
    f.subplots_adjust(wspace=.075, hspace=-.4)

if __name__=='__main__':
    
    #dir = os.path.dirname(__file__)
    #lambda_file= os.path.join(dir, '../scans/allsky/lambda_dict_test_out')
    #lambda2=pickle.load( open(lambda_file, 'r') )

    #redu_mat1, redu_dict1 = redu_data( lambda2, .75, 5)
    
    #f, ax = plt.subplots(3, 4, subplot_kw=dict(projection="mollweide"))

    #for i in [0,1,2]:
    #    for j in [0,1,2,3]:
    #         least_deepsky(ax[i, j], redu_mat1, redu_dict1 )    

    #f.set_size_inches(20,10)
    #ylevel=.08
    #f.text(.11, ylevel, '3 Months', fontsize=20)
    #f.text(.355, ylevel, '6 Months', fontsize=20)
    #f.text(.605, ylevel, '1 Year', fontsize=20)
    #f.text(.85, ylevel, '2 Years', fontsize=20)

    #f.suptitle('Test Title', fontsize=25)
    #f.tight_layout()
    #f.subplots_adjust(wspace=.075, hspace=-.4)

   
    #f.savefig('trial.png')


    dir = os.path.dirname(__file__)
    lambda_file= os.path.join(dir, '../scans/deepsky/lambda_dict_deep_doubleout')

    time1=time.time()
    lambda2=pickle.load( open(lambda_file, 'r') )
    time2=time.time()
    print "Time to load lambda_dict: %s" %(time2-time1)

    out_arr=lam_dict_to_array(lambda2)
    time3=time.time()
    print "Time to run method: %s" %(time3-time2)     

    print out_arr

    f, ax = plt.subplots(1,1, subplot_kw=dict(projection="polar"))

    scat=least_deepsky(ax, out_arr)    

    f.colorbar(scat)
    f.set_size_inches(20,10)
    f.suptitle('Test Title', fontsize=25)
    #f.tight_layout()
    
   
    f.savefig('trial_least_coverage_double.png')

    np.save('saved_array_double', out_arr)   
    time4=time.time()

    print "Time to run plot: %s" %(time4-time3)
