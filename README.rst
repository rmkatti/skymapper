=========
skymapper
=========


**skymapper** is a tool for visualization and analysis of all-sky and 
deep sky scan surveys at desired wavelength ranges. It is built on python's Numpy and Matplotlib libraries 
and the python implementation of the HEALPIX sky discretization algorithm.


**Hits Map of All Sky Scan (Mollweide Projection)**

.. figure:: ./_build/allsky2_complete_1.png
   :align:  center
   :alt: All Sky scan
   :figclass: align-center

   ..


**Hits Map of Deep Sky Scan About North Celestial Pole (Polar Plot)** 

.. figure:: ./_build/phi_365_uniform_fulllambda.png
   :align: center
   :alt: Deep Sky Scan
   :figclass: align-center

   ..
   
Coverage map development requires defining field-of-view (FOV) dimensions, inputing list of pointing directions 
as tuples of (theta, phi, ax), i.e. polar angle, azimuthal angle, and axial angle, and defining the FOV wavelength ranges.
Current implementation defines FOV dimension as a rectangular, 2:1 azimuthal-to-polar linear variable filter with wavelength 
changing across azimuthal direction as sensitivity R (input parameter). Output is a dictionary with wavelength values as keys and 
pixel centers (theta, phi) as values.

Visualization allows two types of coverage maps. Sky regions, collections of sky pixels discretized by HEALPIX algorithm,
viewed multiple are colored corresponding to an increasing viewing redundancy. The all sky map is a Mollweide 
projection (upper picture), and the deep sky map centered around the celestial north pole is a radial projection for
small angles about the pole. 

Analysis identifies areas of missed sky coverage at defined wavelength ranges. Wavelength dictionaries may be converted 
easily to 2D numpy arrays with pixel centers as first two columns, viewing wavelengths as remaining columns, and array
values being redundancy information of sky pixel redundancy at each wavelength. Radial histograms allow binning sky
pixels by radial distance from north celestrial pole for input observing wavelength.


Version Information
--------------------

:Date: 2014-10-8
:Version: 1.0.0
:Authors: Raj Katti

Dependencies
------------

1) **Numpy**

The standard python module for numerical computing: http://www.numpy.org/

2) **Matplotlib**

The standard python module for data visualization: http://matplotlib.org/

3) **Healpix**

Python implementation of the HEALPIX algorithm. Useful for discretization 
of the sky in CMB and astronomy-related work: 

* HEALPIX: http://healpix.jpl.nasa.gov/
* healpy documentation: http://healpy.readthedocs.org/en/latest/
