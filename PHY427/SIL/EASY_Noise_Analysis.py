#!/usr/bin/env python
#########################################
""" 
          Noise analysis

"""
#########################################

import os
import sys
from scipy.stats import norm
import h5py
import time
from optparse import OptionParser
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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
    L1 = p[0]*np.exp(-0.5*L*L)/(2.506628274631001*p[2])
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
    pedestal = np.zeros(nchan)
    noise = np.zeros(nchan)
    nevents = int(options.nevents) # default 128
    minch = int(options.minch) # default 0
    maxch = int(options.maxch) + 1 # default 127 + 1
    # nch = maxch-minch
   
    
    ##################################
    # Open data file the files
    ##################################


    if not os.path.exists(fname):
        print(f"Input file {fname} does not exist")
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
    GT = np.nonzero(T[:]>=0)
    nevts = GT[0].shape[0]
    

    # Reduce the data sample to those events
    print(f"Events in the file. ..................... Nevt= {nevts}")

    TT = GTimer() # This is to show the number of events processed
    TG = GTimer() # This is to profile the process

    ################################
    # Calculate Pedestals 
    ################################
    pedestal = np.mean(SRAW, axis=0) # vector

    #######################################
    # Loop over events to get common noise
    #######################################
        
    #
    # This is to keep the common mode of each event
    #
    C = []
    #
    # Start the timersp
    #     
    TT.start()
    TG.start()
        
    if nevents>0:
        nevts=int(nevents)

    print(f"Events in to analyze. ..................... Nevt= {nevts}")

    SCOR = [[]] * nevts

    nevtot=0.
    noiseCh = np.zeros(nevts)

    for im , ievt in enumerate(GT[0]):
       

        #if TT() >= 0:
        #    print("\r%10d, %10d" % (im, ievt))
        #    sys.stdout.flush()
        #    TT.reset()
        
        ss = np.single(SRAW[im,:]) - pedestal
        cm = np.mean(ss) # common mode shift (scalar)
        cmsig = np.std(ss)
        
        for ich in range(nchan):
            cc = SRAW[im,ich] - pedestal[ich] - cm
            # cc = pedestal[ich] - cm # pc(i,k)
            SCOR[im].append(cc)
            if ich == 40:
               noiseCh[im] = cc

        C.append(cm)
        nevtot += 1
        if nevents>0 and nevtot>=nevts:
            break

    TT.stop()    
    print("\nTotal time elapsed:", TG()    )

    #########################################
    # End Loop over events to get common noise
    #########################################

    ########################################
    # Calculate Pedestals 
    ########################################
    SCOR = np.array(SCOR)
    noise = [np.std(SCOR[:,i], ddof=1) for i in range(nchan)]
    #########################################        
    # PLot some quantities
    ######################################### 

    plt.figure(1)
    
    # The common mode
    # X = np.r_[-50:50:2]
    # plt.subplot(2,1,1)
    # plt.title("Common mode")  
    # plt.xlabel("Channel number")
    # plt.ylabel("ADC counts")
    # plt.plot(range(128), C)
    mu = np.mean(C)
    sigma = np.std(C, ddof=1)
    # n, bins, patches = plt.hist(C,X,color="mediumseagreen")
    # mu, sigma = norm.fit(C)
    # y = norm.pdf(bins, mu, sigma)
    # plt.plot(bins, y, 'r-', linewidth=2)
    # p = Rectangle((0, 0), 1, 1, fc="r")
    # plt.legend([p], [r'$\mu$=%.3f $\sigma$=%.1f' %( mu, sigma)], loc=1)
    
    # plt.subplot(3,1,3)
    plt.xlabel("Event number")
    plt.ylabel("ADC counts")
    isizeC = int(np.size(C))
    X = np.r_[0:isizeC:1]
    plt.plot(X,C,color="mediumseagreen")
    plt.axhspan(mu+sigma, mu+sigma, alpha=1)
    plt.axhspan(mu, mu, alpha=1)
    plt.axhspan(mu-sigma, mu-sigma, alpha=1)
    plt.title("Common Mode")
    plt.show()
    return

  
    plt.figure(2)

    # Pedestals
    X = np.r_[0:128:1]
    plt.subplot(3,1,1)
    plt.title("Pedestal") 
    plt.xlabel("Channel number")
    plt.ylabel("ADC counts") 
    plt.ylim(450,550)
    plt.xlim(0,128)
    plt.bar(X,pedestal,color="mediumseagreen")  
    

    # Noise
    X = np.r_[0:128:1]
    plt.subplot(2,1,2)
    plt.title("Noise vs Channel") 
    plt.xlabel("Channel number")
    plt.ylabel("ADC counts") 
    plt.ylim(0,6)
    plt.xlim(0,128)
    plt.bar(X,noise,color="mediumseagreen") 
    meanN=np.mean(noise[minch:maxch])
    sigmaN = np.std(noise[minch:maxch])
    plt.axhspan(meanN, meanN, alpha=1)
    plt.axhspan(meanN+sigmaN, meanN+sigmaN, alpha=1)
    plt.axhspan(meanN-sigmaN, meanN-sigmaN, alpha=1)
    
    p = Rectangle((0, 0), 1, 1, fc="r")
    plt.legend([p], [r'$\mu$=%.3f $\sigma$=%.1f' %( meanN, sigmaN)], loc=3)
    



    plt.figure(3)

    # Pedestals
    X = np.r_[0:128:1]
    plt.subplot(3,1,1)
    plt.title("Pedestal (estimation from DAC)") 
    plt.xlabel("Channel number")
    plt.ylabel("ADC counts") 
    plt.ylim(450,550)
    plt.xlim(0,128)  
    plt.bar(X,pedestalF,color="mediumseagreen")  
    

    # Noise
    X = np.r_[0:128:1]
    plt.subplot(2,1,2)
    plt.ylim(0,6)
    plt.title("Noise vs Channel (estimation from DAC)") 
    plt.xlabel("Channel number")
    plt.ylabel("ADC counts") 
    plt.ylim(0,6)
    plt.xlim(0,128)  
    plt.bar(X,noiseF,color="mediumseagreen") 


    plt.figure(5)

    # Noise ch 40
    plt.subplot(1,1,1)
    X = np.r_[-20:20:1]
    plt.title("Noise at ch=40")  
    plt.xlabel("ADC counts")
    n, bins, patches = plt.hist(noiseCh,X,density=True,color="mediumseagreen")
    mu, sigma = norm.fit(noiseCh)
    y = norm.pdf(bins, mu, sigma)
    plt.plot(bins, y, 'r-', linewidth=2)
    p = Rectangle((0, 0), 1, 1, fc="r")
    plt.legend([p], [r'$\mu$=%.3f $\sigma$=%.1f' %( mu, sigma)], loc=1)

    plt.show()

    
if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("--nevents",
                      dest="nevents", action="store", type="float",
                      help="Number of events to analyze (DEFAULT ALL)",
                      default=128.
                      )   
    parser.add_option("--maxch",
                      dest="maxch", action="store", type="float",
                      help="Maximum channel for noise analyze (DEFAULT=127)",
                      default=127.
                      )    
    parser.add_option("--minch",
                      dest="minch", action="store", type="float",
                      help="Minimum channel for noise analyze (DEFAULT=0)",
                      default=0.
                      ) 
   
    (options, args) = parser.parse_args()
   


    try:
        main(args[0], options)
    except KeyError:
        print("I need an input file")


