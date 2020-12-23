import pylab
import scipy.integrate as integrate
import numpy as np

"""
    Angular dependency of the strength of a radio wave from a
    half-wavelength dipole antenna aligned with the z-axis
    
"""
np.seterr(divide='ignore', invalid='ignore')

# lambda function: Radiation pattern for a half-wave dipole antenna
func = lambda theta : ( pylab.cos( pylab.pi / 2 * pylab.cos( theta ) ) / pylab.sin( theta ) )**2

# Independent variable / coordinate
theta = pylab.arange( .0, 2*pylab.pi + .025, .025 )

# Normalized antenna pattern
minpatt = 1e-2   # lower thresdhold of the radiation pattern
patt = pylab.tile( minpatt, len( theta ) )
ind = pylab.where( func( theta ) > minpatt )[ 0 ]
if len( ind ) > 0: patt[ ind ] = func( theta[ ind ] )
pattdb = 10. * pylab.log10( patt )

# Set up subplot in polar coordinates
#ax = pylab.subplot( 111, axisbg='Azure', polar=True )
ax = pylab.subplot( 211, polar=True )
ax.grid( True )

# Polar plot
ax.plot( theta, pattdb, label='Half-wave', lw=2 )

titledict = { 'family' : 'serif', 'size' : 14, 'weight' : 'bold' }
ax.set_title( r'Radiation Pattern', fontdict=titledict, va='bottom' )
ax.set_xlabel( r'($\theta$)' )

# discretization of major xticks
tmaj_ticks = pylab.arange( .0, 2 * pylab.pi, pylab.pi / 6. ) 
ax.axes.set_xticks( tmaj_ticks );

ax = pylab.subplot( 212)
ax.plot( theta, pattdb, label='Half-wave', lw=2 )