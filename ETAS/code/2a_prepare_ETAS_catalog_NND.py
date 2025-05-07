#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 13:39:35 2024

@author: rinty
"""

import pandas as pd
import os
import numpy as np
#import re
project_dir = os.getcwd()
main_dir = os.path.dirname(project_dir)
os.chdir(main_dir)

cat_type = str(input())
dir_in = 'data/%s/originals'%cat_type
#dir_in = str(input())
os.chdir(f"{main_dir}/{dir_in}")
files = [f for f in os.listdir() if f.endswith('_org.csv')]

files = sorted(files, key=lambda x: int(x.split('rate')[-1].split('_org.')[0]))

i1 = int(input()) 
i2 = int(input()) 

n1 = i1-1
n2 = i2-1
os.chdir(main_dir)
for i in range(n1, n2):
    #j = i*1
    #file_in = 'simulated_HV_catalog%i.csv'%i 
    #file_in = 'synthetic_variable_rate.csv'
    file_in = files[i]
    print(file_in)
    df = pd.read_csv(f"{dir_in}/{file_in}")
    df['time'] = pd.to_datetime(df['time'])
    df['year'] = df['time'].dt.year.astype(int)
    df['month'] = df['time'].dt.month.astype(int)
    df['day'] = df['time'].dt.day.astype(int)
    df['hour'] = df['time'].dt.hour.astype(int)
    df['minute'] = df['time'].dt.minute.astype(int)
    df['second'] = df['time'].dt.second.astype(int)
    df['microsecond'] = df['time'].dt.microsecond.astype(int)
    df['sec'] = df['second'] + df['microsecond']/1e6
    df['N']     = df.index.astype(int)
    df['sec'] = df['sec'].apply(lambda x: float("{:.2f}".format(x)))
    min_depth = 1
    max_depth = 45
    df['depth'] = np.random.uniform(min_depth, max_depth, size=len(df))
    
    mData_df = pd.DataFrame([df['year'] ,df['month'],df['day'], df['hour'],df['minute'],df['sec'], 
                              df['N'], df['latitude'], df['longitude'],  df['depth'], df['magnitude']]).T
    
    #out_dir = '/Users/rinty/Desktop/Research/ETAS/declustering/data/rate_variable/'
    out_dir = f"{main_dir}/{dir_in}"
    out_dir2 = f"{main_dir}/data/%s/"%cat_type
    #out_dir = f"{main_dir}/data/u20/"
    file_out = file_in.replace('_org.csv', '.csv')
    mData_df.to_csv(f"{out_dir}/{file_out}")
    mData_df.to_csv(f"{out_dir2}/{file_out}")
    print('Number of events: %s'%len(mData_df))


