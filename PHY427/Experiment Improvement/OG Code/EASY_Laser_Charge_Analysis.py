#!/usr/bin/env python
#########################################
""" 
          Laser Charge analysys

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
# Define Landau (Moyal) and error function
#########################################

def fLandau(p, x):
    """ Approximate the landau distribution with the Moyal
        distribution
        
        Parameters:
            p[0] = normalization
            p[1] = mode
            p[2] = width
    """
    L = (x-p[1])/p[2]
    r = p[0]*exp(-0.5*(L+exp(-L)))/2.506628274631001 #math.sqrt(2.0*math.pi)
    return r

def fitLandau(p, x, y):
    """ This is the 'error' function we use for
        the fit.
    """
    return fLandau(p, x) - y
#########################################
# Define Gaussian and error function
#########################################

def fgauss(p, x):
    """ This is a gaussion.
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
    """ Implements the GLib GTimer
    """
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
            
########################################
# Get signal, common noise, noise and S/N
######################################### 
def process_event(ievt, S, nchan, pedestal, noise):
    """ Process a single event
        Returns a tuple with the signal, signal/noise and common mode per chip
    """

    # signal without pedestals
    ss = single(S[ievt,:]) - pedestal
    
    # compute ans subtract common mode
    cm = 0
    cmsig = 0
    ssnew = zeros(nchan)
    chpas = 0
    cmnew = 0
    cmsignew = 0

    # First iteration to get mean and std
    
    cm= mean(ss[0:128])
    cmsig= std(ss[0:128])
 
    # Remove chanells with a charge larger than 3*std 
    
    
    chpas=0
    for ch in range(0, nchan):
        if ss[ch]<(cm+(5*cmsig)):
            ssnew[chpas]= ss[+ch]
            chpas = chpas+1
   # Secon iteration to get mean and std
   
    cmnew = mean(ssnew[0:chpas])
    cmsignew= std(ssnew[0:chpas])

    ss[0:128] -= cmnew 

    cm =cmnew
    sn = ss/noise
   
    return ss, sn, cm


   
#########################################
# Manin Analysis
#########################################

def main(fname,options):  
    

    ##################################
    # Open Pedestal file 
    ##################################

    if not os.path.exists(fname[1]):
        print "Pedestal  file", fname,"does not exist"
        return
    
    F = h5py.File(fname[1],'r')
    
    # Get pedestals and noise
    pedestal = F['/header/pedestal']
    noise    = F['/header/noise']

    ##################################
    # Open data files
    ##################################

    if not os.path.exists(fname[0]):
        print "Input file", fname,"does not exist"
        return
   
    F = h5py.File(fname[0], 'r')


    # Get the signal array
    S = F['/events/signal']

    sncut = float(options.sncut)
    
    # Test that pedestals are OK
    P = mean(S[0:], axis=0)
    pdiff = P - pedestal
    pm = mean(pdiff)
   
    
    # Convert pedestal and noise to "vectors"
    pedestal = pedestal[0,:]
    noise    = noise[0,:]
    sz       = pedestal.shape
    nchan    = sz[0]
   

    #
    # Now process the whole file
    #
    # Get the events with good timing
    
    T     = F['/events/time']
    #
    # Laser data has not time information
    #  

    GT    = nonzero(T[:]>-1)
   

    nevts = GT[0].shape[0]

    print "Loop on Events. ..................... Nevt=", nevts

    TT = GTimer() # This is to show the number of events processed
    TG = GTimer() # This is to profile the process
    
    Ttot = 0.0
    #
    # This is to keep the cluster energy
    #
    G = zeros(0)
    Gnc = zeros(0)
    TCL = zeros(0)
   
    H = zeros(nchan)
    SelCl = zeros(nchan)
    CLsize = zeros(nchan)
    #
    # This is to keep the Hip map
    #
    Hitm = zeros(nchan)
    #
    # This is to keep the charge Cs channel
    #
    Gchan = zeros(nchan)
        
    #
    # This is to keep the common mode of each event
    #
    C = 0
     
    #
    # Start the timers and the main loop
    #     
    TT.start()
    TG.start()

    ########################
    # Loop over events
    ########################
    
    nevtot=0.
    
    for im , ievt in enumerate(GT[0]):
        ic = ievt

        # Process the event
        ss, sn, cm = process_event(ievt, S, nchan, pedestal, noise)
        nevtot= nevtot +1
       
        
        if TT() > 1.0:
            print  "\r%10d, %10d      " % (ievt, nevtot), "Processing .... (event number, total number of events)",
            sys.stdout.flush()
            TT.reset()
            
        # Append the commpn mode.
        C = append(C, cm)
        
        #
        # find the clusters
        #
        used = [ False for x in range(0, nchan) ]
        channels = nonzero(sn>sncut)
        
        nclus = 0
        EClst = zeros(nchan)
        
        for ch in channels[0]:  
            if not used[ch]:
                E=ss[ch]
                nclus= nclus +1 
                EClst[nclus] = ss[ch]
                clst = [ch]
                Hitm [ch] = Hitm [ch] + 1
                used[ch] = True

                for i in range(ch+1, nchan, 1):
                    if sn[i]>sncut and not used[i]:
                        clst.append(i)
                        used[i] = True
                        EClst[nclus] = EClst[nclus] + ss[i]
                        Hitm [i] = Hitm [i] + 1
                    else:
                        break              
    
                if EClst[nclus]>(sncut*1):
                    isz = int(size(clst))
                    CLsize[isz] = CLsize[isz] +1 
  
                SelCl[nclus] = 0
                
        H[nclus] = H[nclus]+1
        
        
        SelCl[nclus] = 1
        
        for i in range(1, nclus+1):
            if EClst[i]>(sncut*1.) and SelCl[nclus]>0.:
                G = append(G, EClst[i])
                TCL = append(TCL, T[ic])
               
    TT.stop()    
    print "\nTotal time elapsed:                 ", TG()
    print "\nTotal events processed in time:     ", nevtot
    
   
    ########################        
    # PLot some quantities
    ########################


    figure(1)
    
    # The common mode
   
    X = r_[-50:50]
    subplot(2,1,1)
    plt.title("Common mode (ADC)")
    plt.ylabel('Number of events')
    plt.xlabel('ADC counts')   
    n, bins, patches = hist(C,X, normed=1,color="mediumseagreen")
    mu, sigma = gaus.fit(C)
    y = normpdf(bins, mu, sigma)
    l = plot(bins, y, 'r-', linewidth=2)
    p = Rectangle((0, 0), 1, 1, fc="r")
    legend([p], [r'$\mu$=%.3f $\sigma$=%.1f' %( mu, sigma)], loc=1)

  

    # The Hip map
    X = r_[0:128:1]
    subplot(2,1,2)
    plt.title("Hit map (Channel)")   
    plt.bar(X,Hitm,color="mediumseagreen")   
 
    figure(2)

    # Pedestals
    X = r_[0:128:1]
    subplot(2,1,1)
    plt.title("Pedestal vs Channel")   
    plt.bar(X,pedestal,color="mediumseagreen")  
    

    # Noise
    X = r_[0:128:1]
    subplot(2,1,2)
    plt.title("Noise vs Channel")   
    plt.bar(X,noise,color="mediumseagreen") 

    figure(3)

    # Charge vs Time
    
    
    # Number of Clusters
    X = r_[0:127:1]
    subplot(2,2,1)
    plt.xlim((0,5))
    plt.title("Number of clusters per event")   
    plt.bar(X,H[:127],color="mediumseagreen")
    Tot=0
    Ntot = 0
    for i in range(0, 127):
        Tot = Tot + i*H[i]
        Ntot = Ntot + H[i]
    if Tot>0:
        Tot =Tot/Ntot
    print "Mean number of cluster in an event",Tot
    
    #  Clusters size 
    X = r_[0:127:1]
    subplot(2,2,2)
    plt.xlim((0,10)) 
    plt.title("Cluster size")   
    plt.bar(X,CLsize[:127],color="mediumseagreen")
    Tot=0
    Ntot = 0
    for i in range(0, 127):
        Tot = Tot + i*CLsize[i]
        Ntot = Ntot + CLsize[i]
    if Tot>0:
        Tot =Tot/Ntot
    print "Mean number of strips  in an cluster",Tot

    figure(4)

    # Data histogram (the landau)
   
    
    X = r_[0:600:6]
    plt.title("Laser")
    plt.ylabel('Number of entries')
    plt.xlabel('ACDs counts')
    plt.xlim(0,600)
    n, bins, patches = hist(G,X,color="mediumseagreen") 
   
 
  

    fit_landau = options.landau

    ibinmax= 6*(int(options.fmax/6))
    ibinmin= 6*(int(options.fmin/6))
    
    X = r_[ibinmin:ibinmax:6]

    
    n, bins, patches = hist(G,X,color = "green")
   
    indx = argmax(n, 0)
    if fit_landau:
        errFunc = fitLandau
        dataFunc = fLandau
        param = [ 0.25*sum(n), bins[indx], 10. ]
    else:
        errFunc = fitGauss
        dataFunc = fgauss
        param = [ sum(n), bins[indx], 10. ]

   
    # Fit to the landau distribution 

    step = 0.5*(bins[1]-bins[0])
    X = bins[:-1] + step
    fit_rc = optimize.leastsq(errFunc, param[:], args=(X, n))
    fit_par = fit_rc[0]
    
    # Draw the fitted curve on top of the histogram
    y = dataFunc(fit_par, X)
    l = plot(X, y, 'r-', linewidth=2, label="hola")
    legend([p],[r'mean  %.1f sigma %.1f' % (fit_par[1], fit_par[2])],'upper right')

    plt.axvspan(options.fmin, options.fmax, alpha=0.20,facecolor='g')
       


    #tight_layout()
    show()

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("--gauss",
                      dest="gauss", action="store_true",
                      help="It will try a gauss fit to the data (default)",
                      default=True
                      )    
    parser.add_option("--landau",
                      dest="landau", action="store_true",
                      help="It will try a Landau-like fit to the data",
                      default=False
                      ) 
    parser.add_option("--fmin",
                      dest="fmin", action="store", type="float",
                      help="Minimum ADC for the fit  (default=0)",
                      default=0.
                      )    
    parser.add_option("--fmax",
                      dest="fmax", action="store", type="float",
                      help="Maximum ADC for the fit  (default=600",
                      default=600.
                      ) 

    parser.add_option("--s/n",
                      dest="sncut", action="store", type="float",
                      help="Signal/Noise cut  (default=5)",
                      default=5.
                      )    
   
    (options, args) = parser.parse_args()
    
    

    if options.landau:
        options.gauss = False
    
    try:
        main(args,options)

    except KeyError:
        print "I need an input file"

