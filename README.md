=== OVERVIEW ===

Ultra-faint Galaxy Likelihood (UGaLi) is a set of python 
classes and functions used to search for ultra-faint satellite 
galaxies of the Milky Way using the stellar object samples 
derived from optical photometric surveys.

Keith Bechtol      <bechtol@kicp.uchicago.edu>
Alex Drlica-Wagner <kadrlica@fnal.gov>

=== USAGE EXAMPLES ===

Examples go here.

=== CODE REPOSITORY ===

https://bitbucket.org/bechtol/ugali/

=== DEPENDENCIES ===

Python packages:
numpy
scipy
pyfits - http://www.stsci.edu/institute/software_hardware/pyfits
healpy - https://github.com/healpy/healpy

emcee  - For MCMC characterization
yaml - http://pyyaml.org/

Mangle:
Not a strict dependency. Used to interface with masks produced by
the Dark Energy Survey Data Mangement group. Download and documentation 
available at http://space.mit.edu/~molly/mangle/

*** Coming soon
astropy - 
emcee - 

Isochrones:
Currently set up to use isochrones in the format produced by Leo Girardi's (Padova)
CMD tool, which has a web interface at http://stev.oapd.inaf.it/cgi-bin/cmd

=== CONVENTIONS ===

Indexing:
array[index_z][index_y][index_x]

Naming:
package_name
module_name.py
ClassName
functionName
variable_name

=== ABBREVIATIONS ===

IMF: initial mass function
CMD: color-magnitude diagram
ROI: region of interest
PDF: probability distribution function
LUT: look-up table
LKHD: likelihood

=== TODO ===

a, b, c = rank by current importance (a > b)
1, 2, 3 = rank by difficulty (1 > 2)

Code:
* (2c) Change name of ugali.utils.projector to ugali.utils.coords
* (2c) Consistent naming convention for pix vs. pixel
* (3c) Consistently make use of angToPix and pixToAng
* (2c) Be careful with spatialBin function when objects fall outside of ROI (CHECK!)
* (1b) Residual maps / how to deal with gradients in background (important mainly for LMC region)
* (1c) Compute observable fraction including photometric errors
* (2c) Check for numerical issues with very small Plummer radii, sampling kernel (ADD WARNING)
* (1b) Investigate large kernel fitting accuracy, what is largest size?
* (1c) Add alternative IMFs
* (2c) Compute the absolute visual magnitude in addition to bolometric luminosity
* (3b) FNAL, Midway, SLAC config files
* (2b) Automated data processing to get mangle masks and catalogs from DESDM
* (2b) Merge config file with default config
* (2b) Switch to astropy for coordinate conversion, etc.
* (1b) Create true composite isochrone (subclassing isochrone) rather than container of isochrones
* (2b) Examine gzipped standard healpix files instead of sparse healpix maps
* (1c) Precompute HEALPix pixel for each object and avoid creating full HEALPix maps
* (2b) SVA1 data products
* (2b) Consider updating DES isochrones
* (2b) Separate calculations from plotting

=== DONE ===
* (1c) Collector function to find peaks (in 3D)
* (2c) Save stellar mass instead of richness?
* (3b) Switch to new kernel
* (2b) SDSS mask
* (2b) SDSS isochrones
* (2b) Have config read yaml files
* (2a) Elliptical kernels
* (2a) Horizontal branch dispersion
* (2b) Subclass the pipeline scripts (at least the argument parsers)
* (3c) Pass 'chatter' argument to logger
* (2a) Config file option for likelihood evaluation radius
* (3b) Rename PDF in kernels
* (3c) Farm should write out config file for future reference
* (3b) Search multiple ROIs in same batch job
* (3b) Distinguish between 'debug' (output verbosity) and 'dryrun' (don't do anything)

=== TEST ===
