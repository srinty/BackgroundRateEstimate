#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:04:32 2024

@author: rinty
"""

import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
from datetime import datetime
import subprocess
import json
project_dir = os.getcwd()
main_dir = os.path.dirname(project_dir)
os.chdir(main_dir)

path =  os.path.join(main_dir,'code')
os.chdir(path)
from define_rates import int_rate as rate
from utils import update_config
rate_type = 'HV_intermediate_rate'    
#================== EDIT CONFIG FILE ===================
i1 = 1
i2 = 2
for i in range(i1,i2):
    year_break =[1981,2003,2025]
    df_merged = pd.DataFrame()
    for j in range(0,len(year_break)):  
    
        config_in = os.path.join(main_dir,'etas-main/config')
        os.chdir(config_in)
        year_start = year_break[j] - 22
        year_end = year_break[j]
        n = rate(year_start)
        #print('bg rate : %s'%n)
        year1 = pd.to_datetime(year_start, format='%Y')
        y1 = year1.strftime('%Y-%m-%d %H:%M:%S')
        year2 = pd.to_datetime(year_end, format='%Y')- pd.Timedelta(days=1)
        y2 = year2.strftime('%Y-%m-%d %H:%M:%S')

        bg_rate_year = 1*n #event/year
        bg_rate_day = bg_rate_year/365.25   #unit: event/day
        #area_CA = 423967
        area_HV = 10431.55
        bg_rate_per_km = bg_rate_day/area_HV #event/day/km2
        

        mu_value =  np.log10(bg_rate_per_km)

        
        p = 1.1 #1.1
        a = 2.3 #2.3 #2.35 
        log_mu = mu_value
        omega = p-1   
        rho = 0.4 #0.4 #0.45
        log_c = -2.95  #np.log10(c)
        d = -0.7 #-0.52#-0.2
        gamma = 1.2
        tau = 3.5
        k0 =  -3.05 #-2.9 #-3.0  
        shape_file ='HV_shape.npy'
        ctype = 'HV'
        params = [ y1,y2, mu_value, a, omega,rho, log_c, d, gamma, tau, k0,]
        inp = [shape_file, ctype, rate_type]
        update_config(params, inp ,i)
        
        temp_dir_out = os.path.join(main_dir,'etas-main/output_data')
        if not os.path.exists(temp_dir_out ):
            os.makedirs(temp_dir_out)
            
        runnable_code = os.path.join(main_dir,'etas-main/runnable_code')
        os.chdir(runnable_code) 
        os.system("python3 simulate_catalog_%s.py"%ctype)

        df = pd.read_csv(f"{temp_dir_out}/{rate_type}/simulated_%s_catalog%i.csv"%(ctype,i))
        print('total events %s'%len(df))
        
        # plt.figure()
        # markers, stems, _ = plt.stem(df['time'], df['magnitude'],linefmt='--', 
        #     markerfmt='o',
        #       basefmt='k--', bottom = 3.0,
        #   )
        # plt.setp(stems, linewidth=0.5, alpha=0.3, color = 'k')
        # plt.setp(markers, markersize=3,markerfacecolor='white', markeredgecolor = 'k', alpha=0.3)

        # plt.title('%s-%s: %s'%(year1,year2,n))
        # plt.show()
        df_merged = pd.concat([df_merged, df])
        print('total merged %s'%len(df_merged))
    df_merged['datetime'] = pd.to_datetime(df_merged['time'])
    df_merged = df_merged.sort_values(by='datetime') 
    df_merged.reset_index(inplace=True, drop=True)
    df_merged['index'] = df_merged.index+1
    out_dir = out_dir = os.path.join(main_dir,'data/%s/originals/'%rate_type)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    print('outdir: %s'%out_dir)
    file_out='synthetic_intermediate_rate%i_org.csv'%i
    df_merged.to_csv(f'{out_dir}/{file_out}')

    
#======= No need to run step 2 separately===========


# ========== Prepare catalog for NND and BG ================
path =  os.path.join(main_dir,'code')
os.chdir(path)


scripts = ['2a_prepare_ETAS_catalog_NND.py','2b_filtered_bg_events.py'] #'script2.py', 'script3.py']

for script in scripts:
    print(f"Running {script} with input  synthetic_catalog{i1}")
    try:
        # Run each script, passing the input file using the subprocess module
        subprocess.run(['python3', script], input=f"{rate_type}\n{i1}\n {i2}\n", text=True)

    except Exception as e:
        print(f"An error occurred while running {script}: {e}")

print("\a")   
        