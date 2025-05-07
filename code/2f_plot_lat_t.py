'''
Created on June, 2024

- plot cluster families with eta <= eta_0 
- plot lat and time (dec. year)

@author: tgoebel - Modifed: Sadia Rinty, University of Memphis
'''
import matplotlib as mpl
#mpl.use( 'Agg') # uncomment for interactive plotting

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#------------------------------my modules-------------------------------------- 
project_dir = os.getcwd()
source_dir = os.path.join(project_dir)
os.chdir(source_dir)
import data_utils as dataIO
#import src.clustering as clustering
from EqCat import EqCat

eqCat   = EqCat() # original catalog
eqCatMc = EqCat() # this catalog will be modified with each Mc iteration
catChild=  EqCat()
catParent= EqCat()

#=================================1==============================================
#                            dir, file, params
#================================================================================
main_dir = os.path.dirname(project_dir)
os.chdir(main_dir)
dir_in = 'data_processed'

input_file = str(input('provide catalog file name:'))
file_in = '%s.mat' %input_file


try:
    b_value_file = file_in.replace( '.mat', '_b_value.txt')
    param_value = pd.read_csv(f"{dir_in}/{b_value_file}")
except:
    param_value =pd.DataFrame({'Mc':np.array([2.5]), 'b':np.array([1])})

plot_dir = 'plots'


dPar  = {   'a_Mc'        : param_value['Mc'].values,   ##np.array( [2.0, 2.5, 3.0, 3.5]),
            #separate clustered and background
            'eta_0'       : -5.0, # run 2_eta_0.py and
                                  # if file exists: default = load this value from ASCII file
            }
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
#print( 'total no. of events', eqCat.size())
eqCat.selectEvents( dPar['a_Mc'][0], None, 'Mag')
#eqCat.selectEvents( tmin, tmax, 'Time')
#print( 'no. of events after initial selection', eqCat.size())

iMc = 0
for f_Mc in dPar['a_Mc']:
    eta_0_file = f"{dir_in}/eta_0.txt" #'%s/%s_Mc_%.1f_eta_0.txt'%(dir_in, file_in, f_Mc)
    # load eta_0 value
    if os.path.isfile( eta_0_file):
        #print( 'load eta_0 from file'),
        f_eta_0 = np.loadtxt( eta_0_file, dtype = float)
        #print( f_eta_0)
    else:
        #print( 'could not find eta_0 file', eta_0_file, 'use value from dPar', dPar['eta_0'])
        f_eta_0 = dPar['eta_0']
    # cut below current completeness
    eqCatMc.copy( eqCat)
    eqCatMc.selectEvents( f_Mc, None, 'Mag')
    #print( 'current catalog size: ',eqCatMc.size())
    # load nearest neighbor distances
    NND_file = '%s_NND_Mc_%.1f.mat'%(os.path.basename( file_in).split('.')[0], f_Mc)
    dNND = dataIO.loadmat( os.path.join( dir_in, NND_file))
    #print( dNND.keys())
    dNND['aNND'] = np.log10( dNND['aNND'])
    #==================================3=============================================
    #                          "declustering" step
    #================================================================================  
    #catChild, catPar = create_parent_child_cat( projCat, dNND)
    catChild.copy( eqCat)
    catParent.copy( eqCat)
    catChild.selEventsFromID( dNND['aEqID_c'], repeats = True)
    catParent.selEventsFromID( dNND['aEqID_p'], repeats = True)
    print( 'tot. ev', eqCatMc.size(), 'parents', np.unique( catParent.data['N']).shape[0], 'children', np.unique( catChild.data['N']).shape[0])
    #==================================4=============================================
    #                          spanning tree
    #================================================================================
    plt.figure( 1)
    ax = plt.subplot(111)  
    for iEv in range( catParent.size()):
        #print( 'MS', int( catParent.data['N'][iEv]), catParent.data['Time'][iEv], eqCatMc.data['Time'][iEv])

        if dNND['aNND'][iEv] < dPar['eta_0']:#triggered cluster
            ax.plot( [catParent.data['Time'][iEv]], [catParent.data['Lat'][iEv]], 'ro', ms = 12, alpha = .2)
            ax.plot( [catParent.data['Time'][iEv],catChild.data['Time'][iEv]],
                      [catParent.data['Lat'][iEv], catChild.data['Lat'][iEv]], 'k-', marker = 'o', ms = 4, mew =1, mfc = 'none')
        else: # independent events
            ax.plot( [catChild.data['Time'][iEv]], [catChild.data['Lat'][iEv]], 'bo', ms = 5, alpha = .6)
    

    #=================================3==============================================
    #                           save results
    #================================================================================

    plt.figure(1)
    plt.savefig( '%s/%s_spanningTree_Mc_%.1f.svg'%(plot_dir, file_in.split('.')[0], f_Mc),dpi = 1000,transparent=True)
    ## save main shock catalog
    #plt.show()
    #plt.clf()


    iMc += 1
