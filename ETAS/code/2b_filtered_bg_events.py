#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:51:16 2024

@author: rinty
"""


import numpy as np
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from scipy import stats
from scipy.stats import gaussian_kde, kstest, gamma
from scipy.stats import variation
from scipy.optimize import curve_fit
import random
import os

project_dir = os.getcwd()
main_dir = os.path.dirname(project_dir)
os.chdir(main_dir)


cat_type = str(input())
dir_in = f'data/{cat_type}'

os.chdir(f"{main_dir}/{dir_in}")
files = [f for f in os.listdir() if f.endswith('.csv')]


files = sorted(files, key=lambda x: int(x.split('rate')[-1].split('.')[0]))


#files.sort()
i1 = int(input()) 
i2 = int(input()) 

n1 = i1-1
n2 = i2-1

for i in range  (n1, n2):
    #i +=1
    file = files[i]
    catalog_name = file[:-4]
    print(catalog_name)
    df_master = pd.read_csv(f"{main_dir}/{dir_in}/{file}")
    try:
        df1 = df_master.drop('Unnamed: 0', axis=1)
    except:
        df1 = df_master
    # df ['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
    # #Add the fractional seconds to the datetime column
    # df['datetime'] = df['datetime'] + pd.to_timedelta(df['sec'], unit='s')
    # df1 = df.sort_values(by='datetime') 
    
    file2 = file.replace('.csv', '_org.csv')
    df2 =  pd.read_csv(f"{main_dir}/{dir_in}/originals/{file2}")
    
    merged_df = pd.merge(df1, df2, on=['latitude', 'longitude', 'magnitude'])
    #merged_df = pd.read_csv(f"{main_dir}/{dir_in}/{file}")

    # Filter where 'background rate' is True in df1
    filtered_df1 = merged_df[merged_df['is_background'] == True]
    filtered_df2 = merged_df[merged_df['is_background'] == False]
    # Select only columns from df2
    df_bg = filtered_df1[df1.columns]
    df_as = filtered_df2[df1.columns]
    out_dir = f"{main_dir}/{dir_in}/originals/"

    file_out1 = file.replace('.csv', '_bg.txt')
    file_out2= file.replace('.csv', '_as.txt')
    df_bg.to_csv(f'{out_dir}/{file_out1}')
    df_as.to_csv(f'{out_dir}/{file_out2}')


