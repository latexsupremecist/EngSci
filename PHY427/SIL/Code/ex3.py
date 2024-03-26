########################################
""" 
          Charge collection analysis

"""
#########################################

import os
import sys
from   scipy.stats import norm
from   scipy import optimize
import h5py
import time
from optparse import OptionParser
from numpy import sum
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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
    r = p[0]*np.exp(-0.5*(L+np.exp(-L)))/2.506628274631001 #sqrt(2.0*pi)
    return r

def fitLandau(p, x, y):
    """ This is the 'error' function we use for
        the fit.
    """
    return fLandau(p, x) - y

########################################
# Define Gaussian and error function
########################################

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
#    Process the event 
# Get signal, common noise, noise and S/N
######################################### 
def process_event(ievt, S, nchan, pedestal, noise):
    
    # signal without pedestals
    ss = np.single(S[ievt,:]) - pedestal
    
    # compute ans subtract common mode
    cm = 0
    cmsig = 0
    ssnew = np.zeros(nchan)
    chpas = 0
    cmnew = 0
    cmsignew = 0

    # First iteration to get mean and std
    
    cm= np.mean(ss[0:128])
    cmsig= np.std(ss[0:128])
 
    # Remove channels with a charge larger than 3*std 
    
    chpas=0
    for ch in range(0, nchan):
        if ss[ch]<(cm+(5*cmsig)):
            ssnew[chpas]= ss[+ch]
            chpas = chpas+1

   # Second iteration to get mean and std
    cmnew = np.mean(ssnew[0:chpas])
    cmsignew= np.std(ssnew[0:chpas])

    ss[0:128] -= cmnew 

    cm =cmnew
    sn = ss/noise
   
    return ss, sn, cm

#########################################
# Manin Analysis
#########################################
def main(fname,options):  
    
    print("HOLA")
    ##################################
    # Open data files
    ##################################    
    
    if not os.path.exists(fname):
        print("Input file", fname,"does not exist")
        return
    
    F = h5py.File(fname, 'r')
    
    
    # Get pedestals and noise
    pedestal = F['/header/pedestal']
    noise    = F['/header/noise']
   

    # Get the signal array
    S = F['/events/signal']

    tmin=float(options.tmin)
    tmax=float(options.tmax)
    sncut = float(options.sncut)
    
    
    # Convert pedestal and noise to "vectors"
    pedestal = pedestal[0,:]
    noise    = noise[0,:]
    sz       = pedestal.shape

    # Get the number of channesl
    nchan    = sz[0]
   
    #
    # Now process the whole file
    #
    # Get the events with good timing
    
    T     = F['/events/time']
    GT    = np.nonzero(T[:]>tmin)
   
    # Now process the whole fileNumber of events in file with good time
    nevts = GT[0].shape[0]
   
    # Reduce the data sample to those events
    print("Loop on Events. ..................... Nevt=", nevts)

    TT = GTimer() # This is to show the number of events processed
    TG = GTimer() # This is to profile the process
    
    Ttot = 0.0
    #
    # This is to keep the cluster energy
    #
    G = np.zeros(0)
    Graw = np.zeros(0)
    Gcal = np.zeros(0)  
            
   
    H = np.zeros(nchan)
    SelCl = np.zeros(nchan)
    CLsize = np.zeros(nchan)
    #
    # This is to keep the Hip map
    #
    Hitm = np.zeros(nchan)
    
    #
    # This is to keep the common mode of each event
    #
    C = 0.
    #
    # Start the timers and the main loop
    #     
    TT.start()
    TG.start()
    
    nevtot=0.

    ########################
    # Loop over events
    ########################
    
    #for im , ievt in enumerate(GT[0]):
    for  ievt in  range(0,1000):
            
        if T[ievt]<=tmin or T[ievt]>tmax :
            continue
        ic = ievt

        # Process the event
        ss, sn, cm = process_event(ievt, S, nchan, pedestal, noise)
        nevtot += 1
        
        
        if TT() > 1.0:
            print("\r%10d, %10d        " % (ievt, nevtot), end="Processing .... (event number, total number of events)")
            sys.stdout.flush()
            TT.reset()

            
        # Append the commpn mode.
        
        C = np.append(C, cm)

        #
        # find the clusters
        #
        used = [False] * nchan
        channels = np.nonzero(sn>sncut)
        
        nclus = 0
        EClst = np.zeros(nchan)
        
        for ch in channels[0]:
            
            if not used[ch]:
                nclus += 1
                EClst[nclus] = ss[ch]
                clst = [ch]
                Hitm [ch] += 1
                used[ch] = True
                    
                for i in range(ch+1, nchan):
                    if sn[i]>sncut and not used[i]:
                        clst.append(i)
                        used[i] = True
                        EClst[nclus] = EClst[nclus] + ss[i]
                        Hitm [i] += 1
                    else:
                        break

                if EClst[nclus]>(sncut*1):
                    isz = int(np.size(clst))
                    CLsize[isz] += 1
                    
  

                SelCl[nclus] = 0
                
                    
        H[nclus] += 1
    
        SelCl[nclus] = 1
        
        
        
        for i in range(1, nclus+1):
            if EClst[i]>(sncut*1.) and SelCl[nclus]>0.:
                G = np.append(G, EClst[i])
                PE0 = options.PE0
                PE1 = options.PE1
                PE2 = options.PE2
                PE3 = options.PE3
                PE4 = options.PE4
                Elec = PE0 + (PE1*EClst[i]) + (PE2*(EClst[i]**2)) +(PE3*(EClst[i]**3))+(PE4*(EClst[i]**4))
                Elec = Elec * 3.67
                if Elec>0.:
                    Elec = Elec/1000
           
                Gcal = np.append(Gcal, Elec)
               
                
                
           
    TT.stop()    
    print("\nTotal time elapsed:                 ", TG())
    print("\nTotal events processed in time:     ", nevtot)
    
   
    ########################        
    # PLot some quantities
    ########################


    plt.figure(1)
    
    # The common mode
    X = np.r_[-50:50]
    plt.subplot(2,1,1)
    plt.title("Common mode (ADC)")
    plt.ylabel('Number of events')
    plt.xlabel('ADC counts')   
    n, bins, patches = plt.hist(C,X, density=True,color="mediumseagreen")
    mu, sigma = norm.fit(C)
    y = norm.pdf(bins, mu, sigma)
    l = plt.plot(bins, y, 'r-', linewidth=2)
    p = Rectangle((0, 0), 1, 1, fc="r")
    plt.legend([p], [r'$\mu$=%.3f $\sigma$=%.1f' %( mu, sigma)], loc=1)
  

    # The Hip map
    X = np.r_[0:128:1]
    plt.subplot(3,1,3)
    plt.title("Hit map (Channel)")  
    plt.ylabel('Number of entries')
    plt.xlabel('Channel number')  
    plt.bar(X,Hitm,color="mediumseagreen")   
 
    plt.figure(2)

    # Pedestals
    X = np.r_[0:128:1]
    plt.subplot(3,1,1)
    plt.title("Pedestal vs Channel")   
    plt.ylabel('Pedestal (ADCs)')
    plt.xlabel('Channel number')  
    plt.bar(X,pedestal,color="mediumseagreen")  
    

    # Noise
    X = np.r_[0:128:1]
    plt.subplot(2,1,2)
    plt.title("Noise vs Channel") 
    plt.ylabel('Noise (ADCs)')
    plt.xlabel('Channel number')    
    plt.bar(X,noise,color="mediumseagreen") 

    plt.figure(3)

    # Number of Clusters
    X = np.r_[0:127:1]
    plt.subplot(2,2,1)
    plt.title("Number of clusters per event")  
    plt.xlabel('Number of cluster')  
    plt.xlim((0,5))
    plt.bar(X,H[:127],color="mediumseagreen")
    Tot=0
    Ntot = 0
    for i in range(0, 127):
        Tot += i*H[i]
        Ntot += H[i]
    if Tot > 0:
        Tot /= Ntot
    
    #  Clusters size 
    X = np.r_[0:127:1]
    plt.subplot(2,2,2)
    plt.title("Cluster size") 
    plt.xlabel('Number of channels') 
    plt.xlim((0,10)) 
    plt.bar(X,CLsize[:127],color="mediumseagreen")
    Tot=0
    Ntot = 0
    for i in range(0, 127):
        Tot += i*CLsize[i]
        Ntot += CLsize[i]
    if Tot>0:
        Tot /= Ntot

    plt.figure(4)

    # Data histogram (the landau)
   
    X = np.r_[0:600:1]
    plt.title("Signal (ADC)")
    plt.ylabel('Number of entries')
    plt.xlabel('Charge (ACDs)')
    plt.ylim(1,100000)
    n, bins, patches = plt.hist(G,X,color="mediumseagreen",log=True)
    
    plt.figure(5)

    # Data histogram (the landau)
    ADCbin=int(options.ADCbin)
    ADCmax=int(options.ADCmax)
    ADCmin=int(options.ADCmin)
    
    X = np.r_[ADCmin:ADCmax:ADCbin]
    plt.title(options.label)
    plt.ylabel('Number of entries')
    plt.xlabel('Charge (ACDs)')
    
    n, bins, patches = plt.hist(G,X,color="mediumseagreen")

    fit_landau = options.landau

    ibinmax= ADCbin*(int(options.fmax/ADCbin))
    ibinmin= ADCbin*(int(options.fmin/ADCbin))
    X = np.r_[ibinmin:ibinmax:ADCbin]
    
    n, bins, patches = plt.hist(G,X,color = 'g')
    indx = np.argmax(n, 0)
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
    plt.plot(X, y, 'r-', linewidth=2, label="hola")
    meann, sigmaa = fit_par[1], fit_par[2]
    plt.legend([r'mean  %.1f sigma %.1f' % (meann, sigmaa)])

    plt.axvspan(options.fmin, options.fmax, alpha=0.20,facecolor='g')
    


    plt.figure(6)

# Data histogram calibrated (the landau)
    Eplotbin=int(options.Eplotbin)
    Eplotmax=int(options.Eplotmax)
    Eplotmin=int(options.Eplotmin)
   
    X = np.r_[Eplotmin:Eplotmax:Eplotbin]
    
    plt.title(options.label) 
    plt.ylabel('Number of entries')
    plt.xlabel('Energy (KeV)')
   
    n, bins, patches = plt.hist(Gcal,X,color="mediumseagreen")
   
    fit_landau = options.landau
 
    Elecmin = options.Emin
    Elecmax = options.Emax
   
    
    ibinEmax= Eplotbin*(int(Elecmax/Eplotbin))
    ibinEmin= Eplotbin*(int(Elecmin/Eplotbin))
   
    X = np.r_[ibinEmin:ibinEmax:Eplotbin]

    n, bins, patches = plt.hist(Gcal,X,color = 'g')
    indx = np.argmax(n, 0)
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
    l = plt.plot(X, y, 'r-', linewidth=2, label="hola")
    plt.legend([p],[r'mode  %.1f sigma %.1f' % (fit_par[1], fit_par[2])])

    plt.axvspan(Elecmin, Elecmax, alpha=0.20,facecolor='g')
    print("Done")    
    plt.show()

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("--gauss",
                      dest="gauss", action="store_true",
                      help="It will try a gauss fit to the data",
                      default=False
                      )    
    parser.add_option("--landau",
                      dest="landau", action="store_true",
                      help="It will try a Landau-like fit to the data (default)",
                      default=True
                      ) 
    parser.add_option("--tmin",
                      dest="tmin", action="store", type="float",
                      help="Minimum TDC to be considered in the analysis (default=0.)",
                      default=0.
                      )  
    parser.add_option("--tmax",
                      dest="tmax", action="store", type="float",
                      help="Maximum TDC to be considered in the analysis (default=100.)",
                      default=100.
                      )   
    parser.add_option("--fmin",
                      dest="fmin", action="store", type="float",
                      help="Minimum ADC for the fit  (default=100)",
                      default=100.
                      )    
    parser.add_option("--fmax",
                      dest="fmax", action="store", type="float",
                      help="Maximum ADC for the fit  (default=250",
                      default=250.
                      ) 
    parser.add_option("--ADCmin",
                      dest="ADCmin", action="store", type="float",
                      help="Minimum ADC for the plot  (default=0)",
                      default=0.
                      )    
    parser.add_option("--ADCmax",
                      dest="ADCmax", action="store", type="float",
                      help="Maximum ADC for the plot  (default=600)",
                      default=600.
                      ) 
    parser.add_option("--ADCbin",
                      dest="ADCbin", action="store", type="float",
                      help="Binning for ADC plot  (default=6)",
                      default=6.
                      ) 
    parser.add_option("--Emin",
                      dest="Emin", action="store", type="float",
                      help="Minimum energy for the fit  (default=70)",
                      default=70.
                      )    
    parser.add_option("--Emax",
                      dest="Emax", action="store", type="float",
                      help="Maximum energy for the fit  (default=200)",
                      default=200.
                      ) 
    parser.add_option("--Eplotmin",
                      dest="Eplotmin", action="store", type="float",
                      help="Minimum Energy for the plot  (default=0)",
                      default=0.
                      )    
    parser.add_option("--Eplotmax",
                      dest="Eplotmax", action="store", type="float",
                      help="Maximum Energy for the plot  (default=300)",
                      default=300.
                      ) 
    parser.add_option("--Eplotbin",
                      dest="Eplotbin", action="store", type="float",
                      help="Binning for Energy plot  (default=3)",
                      default=3.
                      )     
    parser.add_option("--label",
                      dest="label", action="store", type="string",
                      help="Label for the plots  (default=Sr-90)",
                      default="Sr-90"
                      ) 
    parser.add_option("--s/n",
                      dest="sncut", action="store", type="float",
                      help="Signal/Noise cut  (default=5)",
                      default=5.
                      )  
    parser.add_option("--PE0",
                      dest="PE0", action="store", type="float",
                      help=" Parameter 0 to convert ADCs to Energy (default=-270.13)",
                      default=-270.13
                      )     
    parser.add_option("--PE1",
                      dest="PE1", action="store", type="float",
                      help=" Parameter 1 to convert ADCs to Energy (default=160.904)",
                      default=160.904
                      )     
    parser.add_option("--PE2",
                      dest="PE2", action="store", type="float",
                      help=" Parameter 2 to convert ADCs to Energy (default=0.174026)",
                      default=0.174026
                      )  
    parser.add_option("--PE3",
                      dest="PE3", action="store", type="float",
                      help=" Parameter 3 to convert ADCs to Energy (default=-0.000734166)",
                      default=-0.000734166
                      )
    parser.add_option("--PE4",
                      dest="PE4", action="store", type="float",
                      help=" Parameter 4 to convert ADCs to Energy (default=0.00000187504)",
                      default=0.0000018750
                      ) 
        
    (options, args) = parser.parse_args()
    

    

    if options.gauss:
        options.landau = False
    
    try:
        main(args[0], options)
    except KeyError:
        print("I need an input file")


