# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:18:32 2024

@author: i44371
"""

"""
Created on Wed Jun 26 14:58:14 2024

@author: sadia rinty
"""

import numpy as np
import pandas as pd
import os
import matplotlib
#matplotlib.use('MacOSX')
import matplotlib.pyplot as plt

#=================================1==============================================
#                            dir, file, params
#================================================================================
project_dir = os.getcwd()
main_dir = os.path.dirname(project_dir)
os.chdir(main_dir)

dir_in = str(input('data directory:'))

input_file = str(input('provide catalog file name:'))

file_in = '%s.csv' %input_file

data_dir = 'data_processed'

ext = '.csv'

# define catalog type 
catalog_type = 'Formatted' #relocated #'Hazard_Model #ANSS #relocated

plot_dir = os.path.join(main_dir,'plots')

try:
    b_value_file = file_in.replace( ext, '_b_value.txt')
    param_value = pd.read_csv(f"{data_dir}/{b_value_file}")
except:
    param_value =pd.DataFrame({'Mc':np.array([2.5]), 'b':np.array([1])})

f_Mc = param_value['Mc'].values[0]

D = float(input())

eta_file = 'eta_0.txt'#file_in.replace(ext,'.mat_Mc_%.1f_eta_0.txt' %f_Mc)
f_eta_0 = np.loadtxt(f"{main_dir}/{data_dir}/{eta_file}", dtype = float)
#print( 'eta_0',f_eta_0)

file_cluster = file_in.replace(ext, '_Nas_MS_Mc_%.1f.txt'%f_Mc)
#file_cluster = 'h_nonsum_s1_Nas_MS_Mc_2.9.txt'
cluster_cat = np.genfromtxt(f"{main_dir}/{data_dir}/{file_cluster}")
MS_ID = cluster_cat[:,3]

#======= If its the USGS Hazard Model Catalog ====
if catalog_type == 'Hazard_Model':
#0-5 (datetime), 6(ID), 7 (lat), 8 (lon), 9 (depth), 10 (mag)
    new_col_order = [4, 5, 6, 7, 8, 9 ,10, 2, 1, 3,0]
    mData_org = np.loadtxt( f"{dir_in}/{file_in}", usecols=(0,1,2,3,4,5,6,7,8,9,10))
    mData_org[:,10]=(np.arange(0, len(mData_org)))
    mData = (mData_org[:, new_col_order])
    #mData = mData_org
    #print( mData.shape)
    mData = pd.DataFrame(mData)


#======= If its the ANSS Comcat Catalog ====
elif catalog_type == 'ANSS':
    mDateTime     = np.genfromtxt( f"{dir_in}/{file_in}", delimiter=(4,1,2,1,2,1,2,1,2,1,4),
                                            skip_header=1, usecols=(0,2,4,6,8,10)).T
    headDate = ['YR', 'MO', 'DY', 'HR', 'MN', 'SC']
    data =  {}
    for i in range( len(headDate)):
        data[headDate[i]] = mDateTime[i]
    ##2##
    data['N']  = np.arange( len( data['YR']))
    ###3### location, magnitude, gap etc.
    header = ['Lat', 'Lon', 'Depth', 'Mag']#, 'Nst', 'Gap', 'Dmin', 'rms']
    mData = np.loadtxt( f"{dir_in}/{file_in}", delimiter=',', skiprows=1,
                        usecols=(1,2,3,4),#,6,7,8,9),
                        dtype = float).T
    for i in range( len(header)):
        data[header[i]] = mData[i]
    mData = pd.DataFrame.from_dict(data, orient='index').T    


elif catalog_type == 'relocated':               
    mData = np.loadtxt(f"{dir_in}/{file_in}", usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    #print( 'no of columns', mData[0].shape[0])
    #print( 'no. of earthquakes', mData[:,0].shape[0])
    mData = pd.DataFrame(mData)

elif catalog_type == 'Formatted':
    mData = np.loadtxt(f"{dir_in}/{file_in}",delimiter=',', usecols=( 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11),
                        skiprows=1)
    #print( 'no of columns', mData[0].shape[0])
    #print( 'no. of earthquakes', mData[:,0].shape[0])
    mData = pd.DataFrame(mData)

elif catalog_type == 'bootstrap':
    mData = np.loadtxt(f"{dir_in}/{file_in}",delimiter=',', usecols=( 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11),
                        skiprows=1)
    mData[:,6] = np.arange(1, len(mData)+1)
    #print( 'no of columns', mData[0].shape[0])
    #print( 'no. of earthquakes', mData[:,0].shape[0])
    mData = pd.DataFrame(mData)     

#====== Normal from here ====

columns = [ 'year','month', 'day', 'hour','minute', 'sec', 'ID', 'lat','lon', 'depth','mag'] #

mData.columns = columns
#mData['datetime'] = pd.to_datetime(mData[['year', 'month', 'day', 'hour', 'minute']])
# Add the fractional seconds to the datetime column
#mData['datetime'] = mData['datetime'] + pd.to_timedelta(mData['sec'], unit='s')
#mData = mData.sort_values(by='datetime')
#mData = mData[mData['mag']>f_Mc]
mData = mData.reset_index(drop=True)
#mData['index'] = mData.index 
#mData.drop(mData.loc[mData['year']>2017].index, inplace=True)

dData = mData[mData['ID'].isin(cluster_cat[:,3])]
#dData = dData.sort_values(by='datetime')
dData = dData.reset_index(inplace=False,drop=True)
#dData['index'] = dData.index 
outfile = file_in.replace(ext,'_NN.txt')
outfolder = str(input('out folder name:'))
#folder = 'synthetic_declustered_catalog_intermediate_rate_HV'#'declustered_catalog_original'#
directory = f"{main_dir}/{outfolder}"
if not os.path.exists(directory):
    os.makedirs(directory)
dData.to_csv(f"{outfolder}/{outfile}",header=True, index=False)






'''

# Plot the probability density function
plt.figure(1,figsize=(6,6))
ax1 =  plt.subplot(111)

ax1.scatter(mData['year'], mData['index'], s = 6,linewidth=1, color='r', label=f"parent catalog M> %.1f "%f_Mc)
ax1.scatter(dData['year'], dData['index'],  s = 6,linewidth=1, color='b', label=f"NN declustered catalog",)

ax1.set_title('Parent vs Declustered Catalog')
ax1.legend()
ax1.set_xlabel('Time')
ax1.set_ylabel('Cumulative No of Eq')

plt.subplots_adjust(left=0.15, bottom=0.15, right=0.9, top=0.9, wspace=0.1, hspace=0.1)
plt.show()
#plt.savefig( '%s/%s_parent_vs_declustered.png'%(plot_dir,file_in[:-4]),dpi = 500)

'''
