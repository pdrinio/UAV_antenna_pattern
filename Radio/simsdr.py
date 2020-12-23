import pylab
#import scipy.integrate as integrate

class SimSDR:
    def __init__(self):
        pass

    def prx (self,angle):
        lam = 1      # Wavelength
        k = 2*pylab.pi/lam  # Phase constant
        # L = lam    -> phi3dB = 47,8º
        # L = lam/2  -> phi3dB = 78º
        # L = lam/50 -> phi3dB = 90º
        L =1.5*lam
      
        # lambda function: Radiation pattern for a half-wave dipole antenna
        E = lambda theta : pylab.cos(k*L/2*pylab.cos(theta)-pylab.cos(k*L/2))/pylab.sin(theta)
        EdB = 10.*pylab.log10(abs(E(angle*pylab.pi/180)))     
        return (EdB)
