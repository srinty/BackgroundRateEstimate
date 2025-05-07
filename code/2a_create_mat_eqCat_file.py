#!python3.7

#------------------------------------------------------------------------------
import os

#------------------------------my modules-------------------------------------- 
project_dir = os.getcwd()
source_dir = os.path.join(project_dir)
os.chdir(source_dir)
from EqCat import EqCat
import datetime_utils as dateTime
eqCat = EqCat( )

#=================================1==============================================
#                            dir, file, params
#================================================================================
# change to local dir where eq. catalogs are saved
# the original SoCal catalog can be found here: https://scedc.caltech.edu/research-tools/altcatalogs.html
main_dir = os.path.dirname(project_dir)
os.chdir(main_dir)
dir_in = str(input('data directory:'))#'data/synthetic/intermediate_rate_HV/' #'data/data_original' #
input_file = str(input('provide file name:'))
file_in = '%s.csv' %input_file



#=================================2==============================================
#                            load data
#================================================================================
import pandas as pd
df = pd.read_csv(f"{main_dir}/{dir_in}/{file_in}")

import numpy as np

mData1 = np.loadtxt(f"{main_dir}/{dir_in}/{file_in}",delimiter=',', usecols=( 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11),
                    skiprows=1)

mData1[:,6] = np.arange(1,len(mData1)+1)

mData = mData1.T

header = ['YR', 'MO', 'DY', 'HR', 'MN', 'SC','N','Lat', 'Lon','Depth','Mag']
data =  {}
for i in range( len(header)):
    data[header[i]] = mData[i]
    



#print( mData.shape)

eqCat.loadEqCat( f"{main_dir}/{dir_in}/{file_in}", 'Formatted')

print( 'total no. of events: ', eqCat.size())
print( sorted( eqCat.data.keys()))

#=================================3==============================================
#                     test plot and save to .mat binary
#================================================================================
out_dir = 'data_processed'
dir_out = os.path.join(project_dir, out_dir)
os.chdir(out_dir)
eqCat.saveMatBin(file_in.replace( 'csv', 'mat'))
newEqCat = EqCat( )
newEqCat.loadMatBin(file_in.replace( 'csv', 'mat'))
print( newEqCat.size())
print( sorted( newEqCat.data.keys()))







