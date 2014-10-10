"""
Short function for making radial (not deep sky) plots of sky pointings
"""

import matplotlib.pyplot as plt

def plot_points(list_points):
    """
    :param list_points, list of tuples of sky pointings 
        e.g. [(theta1,phi1,ax1), (theta2, phi2, ax2)...]
    """

    theta_vals, phi_vals, psi_vals = zip(*list_points)
    rad_list = [ theta for theta in theta_vals ]
    phi_list = [ phi for phi in phi_vals]

    fig= plt.figure()
    ax= plt.subplot(111, polar=True)
    scat= ax.scatter(phi_list, rad_list, s=10, edgecolors='none')

    plt.show()
