#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 08:51:23 2024

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
from define_rates import stable_rate as rate
from utils import update_config

rate_type = 'HV_stable_rate'    
#================== EDIT CONFIG FILE ===================
i1 = 1
i2 = 2
for i in range(i1,i2):
    
    #config_in = f"{os.environ['HOME']}/Desktop/Research/ETAS/etas-main/config/"
    config_in = os.path.join(main_dir,'etas-main/config')
    os.chdir(config_in)
    
    y1 = "1959-01-01 00:00:00"
    y2 = "2024-12-31 23:59:59"
    n = rate() 
  
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
    #update config outdir line 
    update_config(params, inp ,i)

    temp_dir_out =  os.path.join(main_dir,'etas-main/output_data')
    if not os.path.exists(temp_dir_out):
        os.makedirs(temp_dir_out)
        
    runnable_code = os.path.join(main_dir,'etas-main/runnable_code')
    os.chdir(runnable_code) 
    os.system("python3 simulate_catalog_HV.py")
        

    df = pd.read_csv(f"{temp_dir_out}/{rate_type}/simulated_%s_catalog%i.csv"%(ctype,i))
    print('total events %s'%len(df))

    out_dir = os.path.join(main_dir,'data/%s/originals/'%rate_type)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    print('outdir: %s'%out_dir)
    file_out='synthetic_stable_rate%i_org.csv'%i
    df.to_csv(f'{out_dir}/{file_out}')

    
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

 