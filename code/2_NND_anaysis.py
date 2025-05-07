#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 15:26:17 2024

@author: rinty
"""
import os
import subprocess
import sys


#refresh kernel 
#os.execv(sys.executable, [sys.executable] + sys.argv)

current_dir = os.getcwd()
main_dir = os.path.dirname(current_dir)
code_dir = os.path.join(main_dir, 'code')
os.chdir(code_dir)


data_path = 'data/'
outfolder = os.path.join('data_processed/declustered')

for i in range(1,2):
    #print('running simulation %i'%i)

    j = i*1

    input_file =  'synthetic_stable_rate1'#'HV_ANSS_full_catalog'#


    D = 1.3
 
    # List of Python scripts that require input filenames
    scripts_phase1 = ['2a_create_mat_eqCat_file.py','2b_mag_dist.py']
    scripts_phase2 = ['2c_eta_0.py','2d_NND.py', '2e_dist_tau.py', '2f_plot_lat_t.py',
               '2g_createClust.py','2h_productivity.py',] 
    

    # Loop through each script and run it with the input filename
    for script in scripts_phase1:
        print(f"Running {script} with input file '{input_file}'")
        try:
            # Run each script, passing the input file using the subprocess module
            subprocess.run(['python3', script ],
                            input=f"{data_path}\n{input_file}", text=True)
    
        except Exception as e:
            print(f"An error occurred while running {script}: {e}")


    for script in scripts_phase2:
        print(f"Running {script} with input file '{input_file}'")
        try:
            # Run each script, passing the input file using the subprocess module
            subprocess.run(['python3', script ],
                            input=f"{input_file}\n{D}\n", text=True)
    
        except Exception as e:
            print(f"An error occurred while running {script}: {e}")
    
    sc3 = subprocess.run(['python3',  '2i_create_declustered_catalog.py'], input=f"{data_path}\n{input_file}\n{D}\n{outfolder}\n", text=True)
    print(f'declustering done, file saved in {outfolder}')
    
print("\a")        
    
    
    
    