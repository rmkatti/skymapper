=========
skymapper
=========

.. |fnL| replace:: f\ :sub:`nL` 

**skymapper** is a Python package designed to define, visualize and analyze 
all-sky and deep-sky surveys for SPHEREx, 
an Earth-orbiting spectrophotometer in development at 
Caltech/Jet Propulsion Laboratory. 

.. figure:: ./_build/allsky2_complete_1.png
   :align:  center
   :alt: All Sky scan
   :figclass: align-center

   ..

What is SPHEREx?
----------------
**SPHEREx** stands for **S**\ pectro\ **P**\ hotometer for the **H**\ istory of 
the Universe, **E**\ poch of **R**\ eionization, and Ices **Ex**\ plorer.
Over its two-year mission, SPHEREx will create two near-IR 
sky surveys to address NASA's three major astrophysics goals:

* **Probe the origin and destiny of our universe**

SPHEREx seeks to describe the nature of cosmic inflation, the theorized phase of
of accelerated expansion in the early universe. The mission will produce a 
catalog of low-redshift galaxies to calculate non-Gaussianity in the 
distribution of matter in the universe.
Ultimately, these results will be used to estimate the so-called |fnL| parameter. 
|fnL| > 1 would suggest that several fundamental fields drove inflation, while
|fnL| < 1 would suggest that a single fundamental field drove inflation. 
Either result would be a major advancement in current understanding of the physical universe.  

* **Explore the origin and evolution of galaxies**


* **Discover and study planets around other stars, and explore whether they could harbor life**

What is **skymapper**?
-----------------------

**Hits Map of All Sky Scan (Mollweide Projection)**


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
viewed multiple times are colored corresponding to an increasing viewing redundancy. The all-sky map is a Mollweide 
projection (upper picture), and the deep-sky map centered around the celestial north pole is a radial projection for
small angles about the pole. 

Analysis identifies areas of missed sky coverage at input wavelength ranges. Wavelength dictionaries may be converted 
easily to 2D numpy arrays with pixel centers in first two columns, viewing wavelengths as remaining columns, and array
values being redundancy information of a given sky pixel at a particular wavelength. Radial histograms allow binning sky
pixels by radial distance from north celestrial pole for input observing wavelength.


Version Information
--------------------

:Date: 2014-10-8
:Version: 1.0.0
:Authors: Raj Katti
:Contact: rmkatti@gmail.com

Dependencies
------------

1) **Numpy**

The standard Python library for numerical computing: http://www.numpy.org/

2) **Pandas**

Python library providing high performance data structures and data analysis tools: http://pandas.pydata.org/

3) **Matplotlib**

The standard Python library for data visualization: http://matplotlib.org/

4) **Healpy**

Python implementation of the HEALPIX algorithm. Useful for discretizing the sky
in CMB and astronomy-related work: 

* HEALPIX: http://healpix.jpl.nasa.gov/
* healpy documentation: http://healpy.readthedocs.org/en/latest/

Citations
------------

Bock, J.J. et al. In Press. *\ SPHEREx: An All-Sky Spectral Survey*\ .
California Institute of Technology, Pasadena.
