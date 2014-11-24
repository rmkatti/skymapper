'''
Package Skeleton (of directories):

skymapper/
    gen_maps/

    scans/
        deepsky/
        allsky/

    analyze/

    visualize/

    tests/

Explanation:

gen_maps/ holds the two fundamental classes of skymapper, SkyData and SkyMap2. 

The SkyData class holds hits map information in a 3-tier multiindex Pandas 
dataframe. Tiers 1 and 2 are the angular coordinates (theta,phi) of the pixel
centers. Tier 3 is the possible wavelength (aka lambda) values available to the 
linear variable filter. The fields of these indices are the integer number of 
hits associated with the indices, e.g. number_of_hits_1 corresponds to the 
three-tuple (theta1,phi1,1ambda1), or the number of hits at the pixel centered
at (theta1,phi1) at wavelength lambda1. Given sets of indices, SkyData will
increment the corresponding hits fields by 1. The class allows hits information
to be independent of the structural representation, e.g. dictionary vs Pandas 
dataframe, etc.

The SkyMap2 class takes a scan strategy (a set of pointing directions of the 
field-of-view) and feeds observed pixel centers and their wavelengths to 
a SkyData class. It controls definitions of pixel resolution (w/ HEALPIX 
pixelization algorithm), FOV dimensions, allowed wavelengths 
and time evolution of the scan. The end result of single survey implemented by
SkyMap2 is a completed SkyData class with hits values at each pixel center and
wavelength.


The scans/ folder has two subfolders containing the all-sky and deep sky scan
strategies, in folders allsky/ and deepsky/, respectively. All-sky scans will
be plotted in Mollweide projections, while deep-sky scans will be plotted in
polar projections about the celestial poles. The scan scripts define the 
pointing centers of a particular survey and pass those pointings to the 
SkyMap2 class.


The visualize folder has several definitions scripts for generating hits maps.
The most useful functions are found in plot_points.py. Current implementations
of SkyData and SkyMap2 rely on plot_points functions to plot all-sky and deep-sky 
hits maps. 

The analyze/ folder has functions for extracting figure-of-merits and 
statistics of scans. Unfortunately, most of these functions were built
for a previous implementation of SkyMap2 and SkyData. They have not yet
been updated to the current implementation, but to do so is straightforward
given the ease of accessing all relevant parameters from the SkyData dataframe.


'''


import gen_maps
import tests
import scans
import visualize
import analyze
import data
