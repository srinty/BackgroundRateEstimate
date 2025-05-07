#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:56:23 2023

@author: rinty
"""

import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import os, glob
import pandas as pd
import matplotlib
matplotlib.use('MacOSX')
current_dir = os.getcwd()
main_dir = os.path.dirname(current_dir)
code_dir = os.path.join(main_dir, 'code')
import FMD_GR
from FMD_GR import FMD


os.chdir(main_dir)


# ======== Load the original catalog ==========

dir_in = str(input('data directory:'))#'data/synthetic/intermediate_rate_HV/' #'data/data_original' #
input_file = str(input('provide file name:'))
file_in = '%s.csv' %input_file


catalog_type = 'Formatted' #relocated #ANSS #Hazard_Model


if catalog_type == 'relocated':
    cat = np.loadtxt(f"{dir_in}/{file_in}", usecols=(0,1,2,3,4,5,6,7,8,9,10))
    mag = cat[:,10]
elif catalog_type == 'ANSS':
    cat = np.loadtxt( f"{dir_in}/{file_in}", delimiter=',', skiprows=1,
                        usecols=(1,2,3,4))#,6,7,8,9),#3                    dtype = float)
    mag = cat[:,3]
    
elif catalog_type == 'Hazard_Model':   
    cat = np.loadtxt( f"{dir_in}/{file_in}", usecols=(0,1,2,3,4,5,6,7,8,9, 10,11,12))
    cat = cat[cat[:,4]>1915]
    mag = cat[:,0]
elif catalog_type == 'Formatted':
    
    cat = np.loadtxt(f"{dir_in}/{file_in}",delimiter=',', usecols=( 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
                    skiprows=1)
    #cat = cat[cat[:,0]<2017]
    mag = cat[:,-1]

#=========================================2==================================================================
#                             FMD
#============================================================================================================

oFMD = FMD()
magnitude = mag[~np.isnan(mag)]
print( 'no of events', len(magnitude))
binsize = 0.1

#=====Change Mc limit based on the distribution
mc_type = np.arange(1.0,4.0, binsize)  #"KS" # 

#=========================================2==================================================================
#                             determine Mc and b usign KS-test
#============================================================================================================
# oFMD.data['mag'] = magnitude
# oFMD.get_Mc( mc_type = mc_type)
# oFMD.fit_GR( binCorrection = 0)
# oFMD.mag_dist()

oFMD.data['mag'] = magnitude
a_RanErr = np.random.randn( len(magnitude)) * binsize*.5
oFMD.data['mag'] += a_RanErr
oFMD.get_Mc( mc_type = mc_type)
oFMD.data['mag'] -= a_RanErr

oFMD.mag_dist()
oFMD.fit_GR(binCorrection=binsize*0.1)


print( 'completeness', round( oFMD.par['Mc'], 1))
print( oFMD.par)

#=========================================3==================================================================
#                                plot FMD and KS statistic as fct of Mc
#============================================================================================================

fig, ax = plt.subplots()
ax = plt.subplot(111)
#oFMD.plotDistr(ax)
oFMD.plotFit(ax, 'r')
ax.set_xlim(0, 10)
handles, labels = ax.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))  # Use dictionary to remove duplicates
ax.legend(unique_labels.values(), unique_labels.keys(), loc='upper right')

#plt.show()
out_dir = f"{main_dir}/data_processed"
os.chdir(out_dir)
outfile = file_in.replace( '.csv', '_freq_mag.jpg')
plt.savefig(outfile, format = 'jpg', dpi = 1000)

par = oFMD.par
P = pd.DataFrame.from_dict(par,orient='index')
PP = P.T
PP = PP.apply(lambda x: round(x, 2))
dir_out = os.path.join(main_dir,dir_in)
file_in = file_in.replace( '.csv', '_b_value.txt')
file_out = (f"{out_dir}/{file_in}")
PP.to_csv(file_out)
print( 'save results', file_out)




