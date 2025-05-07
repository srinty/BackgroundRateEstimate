'''
Created on on June, 2024

- compute inter-event times and distance and normalize by magnitude
- create colormap of event-pair density (i.e. NND events) for
    corresponding rescaled event times and distances

@author: tgoebel  #Modified: Sadia Rinty, University of Memphis
'''
import matplotlib as mpl
#mpl.use( 'Agg') # uncomment for interactive plotting

import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import pandas as pd
import matplotlib
from scipy import stats
#matplotlib.use('MacOSX')
#------------------------------my modules-------------------------------------- 
project_dir = os.getcwd()
source_dir = os.path.join(project_dir)
os.chdir(source_dir)
import clustering as clustering
import data_utils as data_utils
from   EqCat import *

eqCat   = EqCat() # original catalog
eqCatMc = EqCat() # this catalog wil be modfied with each Mc iteration
catChild=  EqCat()
catParent= EqCat()
np.random.seed( 123456)
#=================================1==============================================
#                            dir, file, params
#================================================================================
main_dir = os.path.dirname(project_dir)
os.chdir(main_dir)
dir_in = 'data_processed/'

input_file = str(input('provide catalog file name:'))
file_in = '%s.mat' %input_file
try:
    b_value_file = file_in.replace( '.mat', '_b_value.txt')
    param_value = pd.read_csv(f"{dir_in}/{b_value_file}")
except:
    param_value =pd.DataFrame({'Mc':np.array([2.5]), 'b':np.array([1])})

D = float(input())


dPar  = {   'a_Mc'        : param_value['Mc'].values,#np.array( [2.5]),##np.array( [3.0, 3.3, 3.5]),#np.array( [2.0, 2.5, 3.0, 3.5]),
            # fractal dimension and b for eq. (1)
            'D'           : D, # TODO: - these values should be constrained independently
            'b'           :param_value['b'].values[0],#

            
            'rmax' : 200,
            'tmax' : 15,
            #===================smoothing parameters=============
            'binx' : .1, 'biny' : .1,# used for density and gaussian smoothing
            'sigma'   : None, #if None: default = n**(-1./(d+4)),
            #=================plotting==============
            'eta_0'       : -5.0, # run: 2_eta_0.py and
                                  # if eta-0-file exists: default = load this value from ASCII file
            #'xmin' : -13, 'xmax' : 0,

            'Tmin' :  -9, 'Tmax' : -1,
            'Rmin' :  -5, 'Rmax' : 3, #-5, 3
            'cmap' :   plt.cm.jet, }
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize']=14
plt.rcParams['ytick.labelsize']=14
plt.rcParams['axes.labelsize']=14

#=================================2==============================================
#                            load data, select events
#================================================================================
eqCat.loadMatBin(  os.path.join( dir_in, file_in))

eqCat.selectEvents( dPar['a_Mc'][0], None, 'Mag')
#eqCat.selectEvents( tmin, tmax, 'Time')
#print( 'no. of events after initial selection', eqCat.size())

# two ways to do the distance comp: 1 project into equal distance azimuthal , comp Cartersian distance in 3D
#                                   2 get surface distance from lon, lat (haversine), use pythagoras to include depth
eqCat.toCart_coordinates( projection = 'eqdc')

for i in range( dPar['a_Mc'].shape[0]):
    f_Mc =  dPar['a_Mc'][i]
    eta_0_file = f"{dir_in}/eta_0.txt" #'%s/%s_Mc_%.1f_eta_0.txt'%(dir_in, file_in, f_Mc)
    # load eta_0 value
    if os.path.isfile( eta_0_file):
        #print( 'load eta_0 from file'),
        f_eta_0 = np.loadtxt( eta_0_file, dtype = float)
    else:
        #print( 'could not find eta_0 file', eta_0_file, 'use value from dPar', dPar['eta_0'])
        f_eta_0 = dPar['eta_0']
    # cut below current completeness
    eqCatMc.copy( eqCat)
    eqCatMc.selectEvents( f_Mc, None, 'Mag')
    #print( 'current catalog size: ',eqCatMc.size())
    
    # load nearest neighbor distances 
    NND_file = f"{dir_in}/%s_NND_Mc_%.1f.mat"%( file_in.split('.')[0], f_Mc)
    dNND   = data_utils.loadmat(NND_file) #,  struct_as_record=True)

    #==================================3=============================================
    #                       compute re-scaled interevent times and distances
    #================================================================================ 
    catChild.copy( eqCatMc)
    catParent.copy( eqCatMc)
    catChild.selEventsFromID(    dNND['aEqID_c'], repeats = True)
    catParent.selEventsFromID(   dNND['aEqID_p'], repeats = True)
    #print( 'size of offspring catalog', catChild.size(), 'size of parent cat', catParent.size())  

    # note that dictionary dPar here has to include 'b','D' and 'Mc'
    a_R, a_T = clustering.rescaled_t_r( catChild, catParent, {'b':dPar['b'], 'D':dPar['D'], 'Mc':f_Mc}, correct_co_located = True)
    RT_file = f"{dir_in}/%s_RT_Mc_%.1f.mat"%( file_in.split('.')[0], f_Mc)
    scipy.io.savemat( RT_file, {'R' : a_R, 'T': a_T}, do_compression  = True)
    #==================================4==============================================================
    #                       T-R density plots
    #=================================================================================================
    a_Tbin = np.arange( dPar['Tmin'], dPar['Tmax']+2*dPar['binx'], dPar['binx'])
    a_Rbin = np.arange( dPar['Rmin'], dPar['Rmax']+2*dPar['biny'], dPar['biny'])
    XX, YY, ZZ = data_utils.density_2D( np.log10( a_T), np.log10( a_R), a_Tbin, a_Rbin, sigma = dPar['sigma'])
    
    fig1 = plt.figure(1, figsize= (6,7))
    ax = plt.subplot(111)
    #ax.set_title( 'Nearest Neighbor Pairs in R-T')
    #------------------------------------------------------------------------------ 
    normZZ = ZZ*( dPar['binx']*dPar['biny']*eqCatMc.size())
    plot1 = ax.pcolormesh( XX, YY, normZZ, cmap=dPar['cmap'])
    cbar  = plt.colorbar(plot1, orientation = 'horizontal', shrink = .5, aspect = 20,)
    #ax.plot(  np.log10( a_T), np.log10( a_R), 'wo', ms = 1.5, alpha = .2)
    # plot eta_0 to divide clustered and background mode
    ax.plot( [dPar['Tmin'], dPar['Tmax']],  -np.array([dPar['Tmin'], dPar['Tmax']])+f_eta_0, '-', lw = 1.5, color = 'w' )
    ax.plot( [dPar['Tmin'], dPar['Tmax']],  -np.array([dPar['Tmin'], dPar['Tmax']])+f_eta_0,'--', lw = 1.5, color = '.5' )
    
    # ax.plot( [dPar['Tmin'], dPar['Tmax']],  -np.array([dPar['Tmin'], dPar['Tmax']])-4, '-', lw = 1, color = 'w' )
    # ax.plot( [dPar['Tmin'], dPar['Tmax']],  -np.array([dPar['Tmin'], dPar['Tmax']])-5, '-', lw = 1, color = 'w' )
    # ax.plot( [dPar['Tmin'], dPar['Tmax']],  -np.array([dPar['Tmin'], dPar['Tmax']])-6, '-', lw = 1, color = 'w' )
    # ax.plot( [dPar['Tmin'], dPar['Tmax']],  -np.array([dPar['Tmin'], dPar['Tmax']])-7, '-', lw = 1, color = 'w' )
    # ax.plot( [dPar['Tmin'], dPar['Tmax']],  -np.array([dPar['Tmin'], dPar['Tmax']])-8, '-', lw = 1, color = 'w' )
    
    #-----------------------labels and legends-------------------------------------------------------
    #cbar.set_label( 'Event Pair Density [#ev./dRdT]') 
    cbar.set_label( 'Number of Event Pairs',labelpad=-40)
    ax.set_xlabel( 'log Rescaled Time')
    ax.set_ylabel( 'log Rescaled Distance')
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    ax.set_xlim( dPar['Tmin'], dPar['Tmax'])
    ax.set_ylim( dPar['Rmin'], dPar['Rmax'])
    plt.subplots_adjust(left=0.1,bottom=0.05,right=0.9,top=0.9)
    #=================================5==============================================
    #                           save results
    #================================================================================
    #print( 'plot saved in: ','plots/T_R_%s_Mc_%.1f.png'%( file_in.split('.')[0], f_Mc))
    fig1.savefig( 'plots/T_R_%s_Mc_%.1f_b_%.1f_d_%.1f.svg'%( file_in.split('.')[0], f_Mc, dPar['b'],D), dpi = 500)
    #plt.show()
     
    #plt.clf()
    
    fig2, ax = plt.subplots(1,2,figsize=(13,4))
    #ax.plot( vBin, vHist, 'ko')
    ###histogram
    bin_width = 0.2
    aBins       = np.arange( dPar['Rmin'], dPar['Rmax'], bin_width, dtype = float)
    aHist, aBins = np.histogram( np.log10( a_R), aBins)
    aBins = aBins[0:-1] + bin_width*.5
    # correct for binsize
    aHist = aHist/bin_width
    # to pdf (prob. density)
    aHist /= eqCat.size()
    ax[0].bar( aBins, aHist, width =.8*bin_width, align = 'edge', color = '.5', )
    #ax[0].plot( [f_eta_0, f_eta_0], ax.get_ylim(), 'w-',  lw = 2, )
    #ax[0].plot( [f_eta_0, f_eta_0], ax.get_ylim(), 'r--', lw = 2, )

    #ax[0].legend( loc = 'upper left')
    ax[0].set_xlabel( 'log Rescaled Distance, log$_{10} R$')
    ax[0].set_ylabel( 'Number of Events')
    ax[0].grid('on')
    
    # Sort the bins by frequency
    sorted_indices = np.argsort(aHist)[::-1]
    sorted_counts = aHist[sorted_indices]
    sorted_bin_centers = aBins[sorted_indices]
    # Calculate the cumulative sum of the frequencies
    cumulative_counts = np.cumsum(sorted_counts) / np.sum(aHist)
    # Find the mode for the top 95% and 97% of the data
    top_95_index = np.argmax(cumulative_counts >= 0.95)
    top_97_index = np.argmax(cumulative_counts >= 0.97)

    mode_95_R = sorted_bin_centers[np.argmax(sorted_counts[:top_95_index + 1])]

    ax[0].plot([mode_95_R, mode_95_R], ax[0].get_ylim(), 'r--',  lw = 2, label=f'Mode_95%: {mode_95_R:.2f}')
    ax[0].legend()
    
    aBins2       = np.arange( dPar['Tmin'], dPar['Tmax'], bin_width, dtype = float)
    aHist2, aBins2 = np.histogram( np.log10( a_T), aBins2)
    aBins2 = aBins2[0:-1] + bin_width*.5
    # correct for binsize
    aHist2 = aHist2/bin_width
    # to pdf (prob. density)
    aHist2 /= eqCat.size()
    ax[1].bar( aBins2, aHist2, width =.8*bin_width, align = 'edge', color = '.5',)
    #ax[1].legend( loc = 'upper left')
    ax[1].set_xlabel( 'log Rescaled Time, log$_{10} T$')
    #ax[1].set_ylabel( 'Number of Events')
    ax[1].grid('on')
    ax[0].set_xlim( dPar['Rmin'], dPar['Rmax'])
    ax[1].set_xlim( dPar['Tmin'], dPar['Tmax'])
    
    sorted_indices2 = np.argsort(aHist2)[::-1]
    sorted_counts2 = aHist2[sorted_indices2]
    sorted_bin_centers2 = aBins2[sorted_indices2]
    # Calculate the cumulative sum of the frequencies
    cumulative_counts2 = np.cumsum(sorted_counts2) / np.sum(aHist2)
    # Find the mode for the top 95% and 97% of the data
    top_95_index2 = np.argmax(cumulative_counts2 >= 0.95)
    top_97_index2 = np.argmax(cumulative_counts2 >= 0.97)

    mode_95_T = sorted_bin_centers2[np.argmax(sorted_counts2[:top_95_index2 + 1])]

    ax[1].plot([mode_95_T,mode_95_T], ax[1].get_ylim(), 'r--',  lw = 2, label=f'Mode_95%: {mode_95_T:.2f}')
    ax[1].legend()
    
    
    plt.subplots_adjust(left=0.05,bottom=0.12,right=0.95,top=0.9)
    plotFile = 'plots/%s_aR_aT_hist_Mc_%.1f_b_%.1f_d_%.1f.svg'%( file_in.split('.')[0], f_Mc, dPar['b'],D)
    #print( 'save plot', plotFile)
    fig2.savefig( plotFile,dpi = 1000,transparent=True)
    #plt.show()







