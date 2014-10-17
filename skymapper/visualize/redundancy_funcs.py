import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import cPickle as pickle
import numpy as np
from numpy import pi
import os
import collections as coll

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
          
def redu_deepsky(ax, redu_mat, redu_dict, radius_line=5*pi/180):

    '''Plot deepsky redundancy map. Input axis should be type polar.'''
     # Define colormap
    cmap = plt.cm.jet

        # Plot data
    phi_list= redu_mat[:,1]
    rad_list= np.sin(redu_mat[:,0]) 
    scat= ax.scatter(phi_list, rad_list, s=5, c=redu_dict.values(),\
                    cmap=cmap, edgecolors='none')

        # Set and annotate reference radial line
    phi_rad_plot= np.arange(0,2*pi,.01)
    rad_plot = [sin(radius_line)]*len(phi_rad_plot)
    rad_plotter = ax.plot(phi_rad_plot , rad_plot, color='m', linewidth=1)
    ax.annotate('dec=%.2f$^\circ$'%(90-radius_line*180/pi), xy=(-pi/2,sin(radius_line)), xytext=(0.4, 0.2), textcoords='figure fraction', arrowprops=dict(facecolor='green',
	     shrink=.05),bbox=dict(facecolor='blue',alpha=.3) )
    ax.set_rgrids(radii=[ sin(theta) for theta in np.linspace(pi/64,pi/16,3)],labels=90-np.linspace(pi/64,pi/16,3)*180/pi, angle=80, color='DarkOrange',size='medium')
            

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

def subplot_proposal1(f, ax):
    """Implements specs for the subplot proposal1. Input 3x4 subplot fig and axes handles"""

    f.set_size_inches(20,10)
    ylevel=.08
    f.text(.11, ylevel, '3 Months', fontsize=20)
    f.text(.355, ylevel, '6 Months', fontsize=20)
    f.text(.605, ylevel, '9 Months', fontsize=20)
    f.text(.86, ylevel, '1 Year', fontsize=20)

    f.suptitle('All Sky Survey', fontsize=25)
    f.tight_layout()
    f.subplots_adjust(wspace=.075, hspace=-.4)






        
if __name__=='__main__':
    
    dir = os.path.dirname(__file__)
    lambda_file= os.path.join(dir, '../scans/allsky/lambda_dict_test_out')
    lambda2=pickle.load( open(lambda_file, 'r') )

    redu_mat1, redu_dict1 = redu_data( lambda2, .75, 5)
    
    f, ax = plt.subplots(3, 4, subplot_kw=dict(projection="mollweide"))

    for i in [0,1,2]:
        for j in [0,1,2,3]:
            redu_allsky(ax[i, j], redu_mat1, redu_dict1 )    

    f.set_size_inches(20,10)
    ylevel=.08
    f.text(.11, ylevel, '3 Months', fontsize=20)
    f.text(.355, ylevel, '6 Months', fontsize=20)
    f.text(.605, ylevel, '1 Year', fontsize=20)
    f.text(.85, ylevel, '2 Years', fontsize=20)

    f.suptitle('Test Title', fontsize=25)
    f.tight_layout()
    f.subplots_adjust(wspace=.075, hspace=-.4)

   
    f.savefig('trial.png')

