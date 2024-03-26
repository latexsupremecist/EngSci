#!/usr/bin/env python
#########################################
""" 
          Laser Scan analysys

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
#########################################
# Get signal, common noise, noise and S/N
#########################################            

def process_event(ievt, S, nchan, nchip, pedestal, noise):
    """ Process a single event
        Returns a tuple with the signal, signal/noise and common mode per chip
    """
    
    # signal without pedestals
    ss = single(S[ievt,:]) - pedestal
    
    # compute ans subtract common mode
    cm = zeros(nchip)
    cmsig = zeros(nchip)
    ssnew = zeros(nchan*(nchip+1))
    chpas = zeros(nchip)
    cmnew = zeros(nchip)
    cmsignew = zeros(nchip)

    # First iteration to get mean and std
    for i in range(0,nchip):
         cm[i] = mean(ss[128*i:128*(i+1)])
         cmsig[i] = std(ss[128*i:128*(i+1)])
 
    # Remove chanells with a charge larger than 3*std 
    
    for i in range(0,nchip):
        chpas[i]=0
        for ch in range(0, nchan):
            if ss[128*i+ch]<(cm[i]+(5*cmsig[i])):
                ssnew[chpas[i]]= ss[128*i+ch]
                chpas[i] = chpas[i]+1
   # Secon iteration to get mean and std
    for i in range(0,nchip):
         cmnew[i] = mean(ssnew[chpas[i]*i:chpas[i]*(i+1)])
         cmsignew[i] = std(ssnew[chpas[i]*i:chpas[i]*(i+1)])
    
    for i in range(0,nchip):
         ss[128*i:128*(i+1)] -= cmnew[i] 

    cm =cmnew
    sn = ss/noise
    
    return ss, sn, cm

#########################################
# Manin Analysis
#########################################
def main(fname,options):  
    
    
    """ Analyze file fname
    """

    ##################################
    # Open Pedestal file with 
    # name Pedestal_Laser.h5
    ##################################
    
    pfile = fname+'/Pedestal_Laser.h5'
    print "Pedestal File >>>>>>>>>>>>>>>>>:", pfile
    if not os.path.exists(pfile):
        print "Pedestal file", pfile,"does not exist"
        return
    
    F = h5py.File(pfile, 'r')

    # Get pedestals and noise
    pedestal = F['/header/pedestal']
    noise    = F['/header/noise']

    # Convert pedestal and noise to "vectors"
    pedestal = pedestal[0,:]
    noise    = noise[0,:]
    sz       = pedestal.shape
    nchan    = sz[0]
    nchip    = nchan/128
        
    # Convert pedestal and noise to "vectors"Some initializations
    nfiles=int(options.nfiles)
    sncut = float(options.sncut)
    maxch =int(options.maxch)
    minch =int(options.minch)
    nch = maxch-minch+1
   
   

    Charge = []
    for i in range(nch):
        Charge.append([])
        for j in range(nfiles):
            Charge[i].append(0) 
   
    ##################################
    # Open data files with 
    # name Laser_number.h5
    # starting with number=1
    ##################################
   
    star=1
    scont = str(star)
    nfiles = nfiles

    for ifile  in  range(0, nfiles):
        dname = fname+'/Laser_' +scont+'.h5'   
        print "Data File >>>>>>>>>>>>>>>>>>>>>: ", dname    
        if not os.path.exists(dname):
            print "Input file", dname,"does not exist"
            return
    

        F = h5py.File(dname, 'r')

        # Get the signal array
        S = F['/events/signal']
    
        #
        # Now process the whole file
        #

        # Get the events with good timing
    
        T     = F['/events/time']
        GT    = nonzero(T[:]>-1)
   

        nevts = GT[0].shape[0]
    

        # Reduce the data sample to those events
        print "Loop on Events. ..................... Nevt=", nevts

        TT = GTimer() # This is to show the number of events processed
        TG = GTimer() # This is to profile the process
        
        ########################
        # Loop over events
         ########################
        #
        # Start the timers and the main loop
        #     
        TT.start()
        TG.start()
    
        nevtot=0.
        
        for im , ievt in enumerate(GT[0]):

            # Process the event
            ss, sn, cm = process_event(ievt, S, nchan, nchip, pedestal, noise)
            nevtot= nevtot +1
            for ich  in  range(0,  nch):
                ichss= minch+ich
                Charge[ich][ifile] =  Charge[ich][ifile] + ss[ichss]
        
            if TT() > 1.0:
                print  "\r%10d, %10d      " % (ievt, nevtot), "Processing .... (event number, total number of events)",
                sys.stdout.flush()
                TT.reset()
      
        for ich  in  range(0,  nch):
            if nevtot>0:
                 Charge[ich][ifile]  =  Charge[ich][ifile] /nevtot
    
        ########################
        # End Loop over events
        ########################
        star=star+1
        scont = str(star)

        TT.stop()    
        print "\nTotal time elapsed:                 ", TG()
        print "\nTotal events processed in time:     ", nevtot
  
    
    ########################        
    # PLot some quantities
    ########################

    figure (1)
    
    plt.title("Laser scan ") 
    plt.xlabel('Laser steps (x 10 microns)')
    plt.ylabel('ADCs')
    isetup = 0
    col = ['b', 'r', 'g', 'k']
    mk = ['s', 'o', '^', '+']
    ls = ['-', '--', ':', '-.']
    for i in range(0,nch):
        ifig= i+1
        # figure(ifig)
        X = r_[0:nfiles:1]
        
        if isetup<4:
            plt.plot(X,Charge[i][:], marker=mk[isetup], linestyle=ls[isetup],color=col[isetup],lw=2, ms=6)
        else:
            isetup = -1
        isetup = isetup +1
    show()

    
if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("--nfiles",
                      dest="nfiles", action="store", type="float",
                      help="Number of files to read (default=1)",
                      default=1
                      )   
    parser.add_option("--maxch",
                      dest="maxch", action="store", type="float",
                      help="Channel maximum (default=127)",
                      default=127.
                      )    
    parser.add_option("--minch",
                      dest="minch", action="store", type="float",
                      help="Channel minimum (default=0)",
                      default=0.
                      ) 
    parser.add_option("--s/n",
                      dest="sncut", action="store", type="float",
                      help="Signal/Noise cut  (default=5)",
                      default=5.
                      )    
   
    (options, args) = parser.parse_args()
   


    try:
        main(args[0], options)
    except KeyError:
        print "I need an input file"


