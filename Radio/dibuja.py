#%pylab
#import matplotlib.pyplot as plt
import numpy as np
import pylab

theta, power = np.loadtxt('medidas.txt', delimiter=',', unpack=True)
theta = theta*pylab.pi/180

minpow = -50 # lower thresdhold of the radiation pattern
ind = pylab.where( power < minpow )[ 0 ]
if len( ind ) > 0: power[ ind ] = minpow

theta, power = zip(*sorted(zip(theta, power)))

theta = np.asarray(theta) # convierto tupla en ndarray
power = np.asarray(power)

# Set up subplot in polar coordinates
ax = pylab.subplot(211, polar=True)
ax.grid( True )

# Polar plot
ax.plot(theta, power, label='Diagrama de radiación', lw=2)


titledict = { 'family' : 'serif', 'size' : 14, 'weight' : 'bold' }
ax.set_title( r'Radiation Pattern', fontdict=titledict, va='bottom' )
ax.set_xlabel( r'($\theta$)' )

# discretization of major xticks
tmaj_ticks = pylab.arange( .0, 2 * pylab.pi, pylab.pi / 6. ) 
ax.axes.set_xticks( tmaj_ticks );

ax = pylab.subplot(212)
ax.grid( True )
ax.plot(theta*180/pylab.pi, power, label='Half-wave', lw=2)