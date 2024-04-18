#!/usr/bin/env python
#########################################
""" 
          Noise analysys

"""
#########################################

import os
import sys
from   pylab import *
from   scipy.stats import norm as gaus
from   scipy import optimize
import h5py
import time
import math
from optparse import OptionParser
from numpy import sum
import matplotlib.pyplot as plt
import numpy as np


#########################################
# Define Gaussian and error function
#########################################
def fgauss(p, x):
    """ This is a gaussian.
        Parameters:
           p[0] = maximum
           p[1] = mean
           p[2] = sigma
    """
    L  = (x-p[1])/p[2]
    L1 = p[0]*exp(-0.5*L*L)/(2.506628274631001*p[2])
    return L1

def fitGauss(p, x, y):
    """ The error function
    """
    return fgauss(p, x) - y


#########################################
# Implements the GLib GTimer
#########################################
class GTimer(object):
    
    def __init__(self):
        self._start = 0
        self._end = 0
        self._running = False
        
    def start(self):
        self._start = time.time()
        
    def __call__(self):
        if self._running:
            return time.time() - self._start
        
        else:
            return 0.0
        
    def start(self):
        self._start = time.time()
        self._running = True
        
    def stop(self):
        self._running = False
        
    def reset(self):
        if self._running:
            self._start = time.time()
            
#########################################
# Manin Analysis
#########################################
def main(fname,options):  
    
    ##################################
    # Inizialitation
    ##################################
    nchan= 128
    pedestal = zeros(nchan)
    noise = zeros(nchan)
    nevents=int(options.nevents)
    maxch =int(options.maxch)+1
    minch =int(options.minch)
    nch = maxch-minch
    noiseCh = zeros(nevents)
   
    
    ##################################
    # Open data file the files
    ##################################


    if not os.path.exists(fname):
        print "Input file", fname,"does not exist"
        return
    F = h5py.File(fname, 'r')
        
    # Get pedestals and noise from DAC
    pedestalF = F['/header/pedestal']
    noiseF    = F['/header/noise']
        
    # Convert pedestal and noise from DAC to "vectors"
    pedestalF = pedestalF[0,:]
    noiseF    = noiseF[0,:]

    # Get the signal array
    SRAW = F['/events/signal']

    # Get the events with good timing
    
    T = F['/events/time']
    GT    = nonzero(T[:]>=0)
    nevts = GT[0].shape[0]
    

    # Reduce the data sample to those events
    print "Events in the file. ..................... Nevt=", nevts

    TT = GTimer() # This is to show the number of events processed
    TG = GTimer() # This is to profile the process

    ################################
    # Calculate Pedestals 
    ################################
    pedestal = mean(SRAW[0:],axis=0)

    #######################################
    # Loop over events to get common noise
    #######################################
        
    #
    # This is to keep the common mode of each event
    #
    C = 0
    #
    # Start the timersp
    #     
    TT.start()
    TG.start()
        
    if nevents>0:
        nevts=int(nevents)

    print "Events in to analyze. ..................... Nevt=", nevts

    SCOR = [[] for _ in range(nevts)]
    nevtot=0.
    noiseCh = zeros(nevts)

    for im , ievt in enumerate(GT[0]):
       

        if TT() >= 0:
            print "\r%10d, %10d" % (im, ievt),
            sys.stdout.flush()
            TT.reset()
        
        ss = single(SRAW[ievt,:]) - pedestal
        cm = mean(ss[0:128])
        cmsig = std(ss[0:128])
        
        for ich in range(0,nchan):
            cc= SRAW[ievt,ich]-pedestal[ich]-cm
            SCOR[ievt].append(cc)
            if ich<41 and ich>39.:
                noiseCh[ievt]=cc

        C = append(C, cm)
        nevtot= nevtot +1
        if nevents>0 and nevtot>=nevts:
            break  

    TT.stop()    
    print "\nTotal time elapsed:", TG()    
    #########################################
    # End Loop over events to get common noise
    #########################################

    ########################################
    # Calculate Pedestals 
    ########################################
    noise = std(SCOR[0:],axis=0)
       
    
    #########################################        
    # PLot some quantities
    ######################################### 

    figure (1)
    
    # The common mode
    X = r_[-50:50:2]
    
    subplot(2,1,1)
    plt.title("Common mode")  
    plt.xlabel("Channel number")
    plt.ylabel("ADC counts")
    n, bins, patches = hist(C,X, normed=1,color="mediumseagreen")
    mu, sigma = gaus.fit(C)
    y = normpdf(bins, mu, sigma)
    l = plot(bins, y, 'r-', linewidth=2)
    p = Rectangle((0, 0), 1, 1, fc="r")
    legend([p], [r'$\mu$=%.3f $\sigma$=%.1f' %( mu, sigma)], loc=1)
    
    subplot(3,1,3)
    plt.xlabel("Event number")
    plt.ylabel("ADC counts")
    isizeC = int(size(C))
    X = r_[0:isizeC:1]
    plt.plot(X,C,color="mediumseagreen")
    axhspan(mu, mu, alpha=1)
    axhspan(mu+sigma, mu+sigma, alpha=1)
    axhspan(mu-sigma, mu-sigma, alpha=1)

  
    figure(2)

    # Pedestals
    X = r_[0:128:1]
    subplot(3,1,1)
    plt.title("Pedestal") 
    plt.xlabel("Channel number")
    plt.ylabel("ADC counts") 
    plt.ylim(450,550)
    plt.xlim(0,128)
    plt.bar(X,pedestal,color="mediumseagreen")  
    

    # Noise
    X = r_[0:128:1]
    subplot(2,1,2)
    plt.title("Noise vs Channel") 
    plt.xlabel("Channel number")
    plt.ylabel("ADC counts") 
    plt.ylim(0,6)
    plt.xlim(0,128)
    plt.bar(X,noise,color="mediumseagreen") 
    meanN=mean(noise[minch:maxch])
    sigmaN = std(noise[minch:maxch])
    axhspan(meanN, meanN, alpha=1)
    axhspan(meanN+sigmaN, meanN+sigmaN, alpha=1)
    axhspan(meanN-sigmaN, meanN-sigmaN, alpha=1)
    
    p = Rectangle((0, 0), 1, 1, fc="r")
    legend([p], [r'$\mu$=%.3f $\sigma$=%.1f' %( meanN, sigmaN)], loc=3)
    



    figure(3)

    # Pedestals
    X = r_[0:128:1]
    subplot(3,1,1)
    plt.title("Pedestal (estimation from DAC)") 
    plt.xlabel("Channel number")
    plt.ylabel("ADC counts") 
    plt.ylim(450,550)
    plt.xlim(0,128)  
    plt.bar(X,pedestalF,color="mediumseagreen")  
    

    # Noise
    X = r_[0:128:1]
    subplot(2,1,2)
    plt.ylim(0,6)
    plt.title("Noise vs Channel (estimation from DAC)") 
    plt.xlabel("Channel number")
    plt.ylabel("ADC counts") 
    plt.ylim(0,6)
    plt.xlim(0,128)  
    plt.bar(X,noiseF,color="mediumseagreen") 


    figure(5)

    # Noise ch 40
    subplot(1,1,1)
    X = r_[-20:20:1]
    plt.title("Noise at ch=40")  
    plt.xlabel("ADC counts")
    n, bins, patches = hist(noiseCh,X,normed=1,color="mediumseagreen")
    mu, sigma = gaus.fit(noiseCh)
    y = normpdf(bins, mu, sigma)
    l = plot(bins, y, 'r-', linewidth=2)
    p = Rectangle((0, 0), 1, 1, fc="r")
    legend([p], [r'$\mu$=%.3f $\sigma$=%.1f' %( mu, sigma)], loc=1)

    show()

    
if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("--nevents",
                      dest="nevents", action="store", type="float",
                      help="Number of events to analyce (DEFAULY ALL)",
                      default=0.
                      )   
    parser.add_option("--maxch",
                      dest="maxch", action="store", type="float",
                      help="Maximum channel for noise analyce (DEFAULY=127)",
                      default=127.
                      )    
    parser.add_option("--minch",
                      dest="minch", action="store", type="float",
                      help="Minimum channel for noise analice (DEFAULY=0)",
                      default=0.
                      ) 
   
    (options, args) = parser.parse_args()
   


    try:
        main(args[0], options)
    except KeyError:
        print "I need an input file"


