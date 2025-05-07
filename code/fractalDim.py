#!bin/python3.7
"""

        - Correlation Integrals:

        TODO: box count

        References:
        -Hirata, T. (1989). Fractal dimension of fault systems in Japan:
        Fractal structure in rock fracture geometry at various scales.
        Pure and Applied Geophysics PAGEOPH, 131(1–2), 157–170.
        https://doi.org/10.1007/BF00874485
        -Hirata, T. (1989). A correlation between the b~value and the
        fractal dimension of earthquakes. J. Geophys. Res., 94, 7507–7514.
        -Wyss, M., Sammis, C. G., Nadeau, R. M., & Wiemer, S. (2004). Fractal
        dimension and b-value on creeping and locked patches of the San Andreas
        fault near Parkfield, California. Bull. Seismol. Soc. Am., 94, 410–421.
        -Goebel, T. H. W., Kwiatek, G., Becker, T. W., Brodsky, E. E., & Dresen, G. (2017).
        What allows seismic events to grow big?: Insights from b-value and fault roughness
        analysis in laboratory stick-slip experiments. Geology, 45(9), 815–818.
        https://doi.org/10.1130/G39147.1
"""
import numpy as np
import scipy.io

def C_r_Int( a_X, a_Y, a_Z = None, **kwargs):
    """ compute pair correlation function in 2D
    1) compute distance between all event pair combination
    2) use log-bin vector to count events within distance range
        a) N(s<r)
        b) N(s>rmin, s<rmax)
    3) get average event numbers and normalize to one
    - faster implementation of massBased which includes random sampling and uncertainty estimates
    Input:
        a_X, a_Y, a_Z = None
        kwarks:
            'x_min','x_max' = distance range for point density count
            'logBinning'    = False (default) toggle between linear and log bins
            'binFactor'     = 1.4 (default) only with logBinning
                                binFactor = a_Bins[1]/a_Bins[0]

    """
    Nmin        = 3 # used to determine lower end of linear portion
    maxNoBins   = 30 # only used for linear binning
    N           = a_X.shape[0]
    # defaults for kwargs
    x_min,x_max = .1,15
    binFactor   = 1.2
    if 'x_min' in kwargs.keys() and kwargs['x_min'] is not None:
        x_min = kwargs['x_min']
    if 'x_max' in kwargs.keys() and kwargs['x_max'] is not None:
        x_max = kwargs['x_max']
    if 'binFactor' in kwargs.keys() and kwargs['binFactor'] is not None:
        binFactor = kwargs['binFactor']
    if 'logBinning' in kwargs.keys() and kwargs['logBinning'] is not None and kwargs['logBinning'] != False:
        a_Bins = 10**np.arange( np.log10(x_min), np.log10(x_max), np.log10(binFactor))
    else:#simple fractions of initial bin
        a_Bins = np.arange( x_min, x_max,  (x_max-x_min)/maxNoBins, dtype = float)
    a_Bins = np.hstack( (0, a_Bins))
    mN_Events = np.zeros( ( N, a_Bins.shape[0]-1) ) #rows are #no of events for each bin or radii
    mN_evSum  = np.zeros( ( N, a_Bins.shape[0]-1) )
    for i in range(N):
        # compute distance between current point and all other points
        if a_Z is not None:
            a_R = np.sqrt((a_X[i] - a_X) ** 2 + (a_Y[i] - a_Y) ** 2 + (a_Z[i] - a_Z) ** 2)
        else:
            a_R = np.sqrt((a_X[i] - a_X) ** 2 + (a_Y[i] - a_Y) ** 2)
        for m in range( a_Bins.shape[0]-1):
            # sel = np.logical_and(a_R > a_Bins[m], a_R < a_Bins[m + 1])
            # # count events within radius
            # mN_Events[i, m] = sel.sum()
            sel_cum = a_R < a_Bins[m + 1]
            mN_evSum[i, m] = sel_cum.sum()
    #------------ determine minimum cut-off----------------------
    aN_ave  = mN_evSum.mean(axis=0)
    sel_N   = aN_ave >= Nmin
    dResults = {}  # dictionary that contains results
    dResults['aL_ave']   = a_Bins[1::][sel_N] #+ dResults['aDeltaL']*.5
    dResults['aN_ave']   = aN_ave[sel_N]
    dResults['aN_sum']   = mN_evSum.sum( axis=0)[sel_N]
    dResults['aCorr']    = mN_evSum.sum( axis=0)[sel_N]/N**2
    #dResults['aN_disc']  = mN_Events.mean(axis=0)#/aN_evDisc.max()
    return dResults

def C_r_3D( vX, vY, vZ, **kwargs):
    """ compute pair correlation function in 3D cartesian coordinates
        kwargs: randomSamples = int - use only subset of data to speed up the process
                logBinning    = default: True
                binFactor     = factor that separates log-bins default: 2
                x_min, x_max  = limits for vector with log distances 
    """
    maxNoBins = 30
    N         = vX.shape[0]
    if 'randomSampling' in kwargs.keys() and kwargs['randomSampling'] != False and  kwargs['randomSampling'] is not None:
        N = kwargs['randomSampling']
        randSamp = True
    else:
        randSamp = False
    print( 'samples', N, 'catalog size', vX.shape[0])
    if 'x_min' in kwargs.keys() and kwargs['x_min'] is not None:
        x_min = kwargs['x_min']
    else:
        x_min = .1 
    if 'x_max' in kwargs.keys() and kwargs['x_max'] is not None:
        x_max = kwargs['x_max']
    else:
        x_max = 15 
    if 'binFactor' in kwargs.keys() and kwargs['binFactor'] is not None:
        binFactor = kwargs['binFactor']
    else:
        binFactor = 2
    if 'logBinning' in kwargs.keys() and kwargs['logBinning'] is not None and kwargs['logBinning'] != False:
        #vBins =  algebra.createLogVector(  x_ini = x_min, x_max = x_max, binFactor = binFactor)
        if 'Nbins' in kwargs.keys() and kwargs['Nbins'] is not None:
            vBins = algebra.createNpLogVector( kwargs['Nbins'], **kwargs)
        else:
            vBins = algebra.createNpLogVector( maxNoBins, **kwargs)
    else:#simple fractions of initial bin
        vBins = np.arange( x_min, x_max,  (x_max-x_min)/maxNoBins, dtype = float)
    vBins = np.hstack( (0, vBins))
    dResults  = { 'mN_Events':np.array([]),'aN_std':np.zeros(vBins.shape[0]-1)}#dictionary that contains results
    mN_Events = np.zeros( ( N,  vBins.shape[0]-1) ) #rows are #no of events for each bin or radii
    mN_evSum  = np.zeros( ( N,  vBins.shape[0]-1) )
    # get distances between all vectors (N2 vectors and distances)
    # count events within vBins anuli
    if randSamp == True:
        #print( N
        for i in range( N):
            #compute distance between current point and all other points
            vRan = np.random.random_integers(0, vX.shape[0]-1, vX.shape[0])
            currX,currY,currZ = vX[vRan],vY[vRan],vZ[vRan]
            vDistance = np.sqrt( (vX[i] - vX)**2 + (vY[i] - vY)**2 + (vZ[i] - vZ)**2)
            for m in range(  vBins.shape[0]-1):
                sel = np.logical_and( vDistance > vBins[m], vDistance < vBins[m+1])
                #count events within radius and append to vector
                mN_Events[i,m] = sel.sum()   
                sel_cum = vDistance < vBins[m+1]
                mN_evSum[i,m]  = sel_cum.sum()        
    else:
        for i in range( N):
            #compute distance between current point and all other points
            vDistance = np.sqrt( (vX[i] - vX)**2 + (vY[i] - vY)**2 + (vZ[i] - vZ)**2)
            for m in range(  vBins.shape[0]-1):
                sel = np.logical_and( vDistance > vBins[m], vDistance < vBins[m+1])
                #count events within radius and append to vector
                mN_Events[i,m] = sel.sum()   
                sel_cum = vDistance < vBins[m+1]
                mN_evSum[i,m]  = sel_cum.sum()
    dResults['aDeltaL']  = vBins[1::]-vBins[0:-1]
    dResults['aL_ave']   = vBins[1::] + dResults['aDeltaL']*.5
    dResults['aN_ave']   = mN_Events.mean(axis=0)
    dResults['aN_sum']        = mN_Events.sum( axis=0)
    dResults['aN_aveCumNo']   = mN_evSum.mean( axis=0)
    dResults['aN_sumCumNo']   = mN_evSum.sum( axis=0)
    return dResults

    
    
    
    
            
         