#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 12:59:45 2025

@author: rinty
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from scipy import stats
from scipy.stats import gaussian_kde, kstest, gamma
from scipy.stats import variation
from scipy.optimize import curve_fit
import random
import os
from datetime import datetime, timedelta



project_dir = os.getcwd()
main_dir = os.path.dirname(project_dir)
os.chdir(main_dir)
plot_dir = os.path.join(main_dir, 'plots')
dir_in = 'data/' 
os.chdir(f"{main_dir}/{dir_in}")

file = 'HV_ANSS_full_catalog.csv'

code_dir = os.path.join(main_dir, 'code')
os.chdir(code_dir)
from plot_utils import decimal_year_to_datetime


# I have the reasenberg declustered catalog as well to compare. 
r85_in = 'r85' 
declustered_in = 'data_processed/declustered' 

#==== comment out to run all files
fig = plt.figure(figsize=(14,8))
gs = fig.add_gridspec(2, 2)

ax1 = fig.add_subplot(gs[0, :])
ax3 = fig.add_subplot(gs[1, :]) 
ax4 = ax3.twinx()

#==== comment out to run all files

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 16
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize']=16
plt.rcParams['ytick.labelsize']=16
plt.rcParams['axes.labelsize']=16
minorTick = {'which': 'minor', 'direction': 'out', 'length': 4, 'width': 1}
majorTick = {'which': 'major', 'direction': 'out', 'length': 8, 'width': 2}

colors = ['red', 'green', 'blue']

approaches = ["Gamma", "NN", "R85"]

b_value_file = file.replace( '.csv', '_b_value.txt')

param_value = pd.read_csv(f"{main_dir}/data_processed/{b_value_file}")
f_Mc = param_value['Mc'].values[0]
print(f'Mc:{f_Mc}')


catalog_name = file[:-4]
print(catalog_name)
df_master = pd.read_csv(f"{main_dir}/{dir_in}/{file}")
#df = df_master[df_master['year']<2018]
df = df_master
df ['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
#Add the fractional seconds to the datetime column
df['datetime'] = df['datetime'] + pd.to_timedelta(df['sec'], unit='s')
df = df.sort_values(by='datetime') 
df = df[df['magnitude']>=f_Mc]
df.reset_index(inplace=True, drop=True)
df['index'] = df.index+1

df['inter_event_time'] = df['datetime'].diff().dt.total_seconds()/ (24 * 3600)

df['decimalyear'] = df['datetime'].dt.year + df['datetime'].dt.dayofyear / 365.25

# Drop the first NaN value resulting from the diff operation
df = df.dropna(subset=['inter_event_time'])
    
N = len(df)
T_days = (df['datetime'].max()- df['datetime'].min()).days
T_years = (df['datetime'].max().year- df['datetime'].min().year)
years = np.arange(df['datetime'].min().year, df['datetime'].max().year+1)

#create dictionary for errors and rate 
error_dict = {approach: pd.DataFrame(index=years) for approach in approaches}
rate_dict = {approach: pd.DataFrame(index=years) for approach in approaches}

total_eq_rate_days = N / T_days
total_eq_rate_year = N / T_years

seismicity_rate_per_year = df.groupby('year').size()
 
df = df[df['inter_event_time'] != 0]
#===----- No need to normalize the inter event time -------
inter_event_times = df['inter_event_time'].values #* total_eq_rate_days

#===== compute background fraction as per Paper Heinzl 2006 ==========
tau_mean = np.mean(inter_event_times)
tau_var = np.var(inter_event_times)
tau_sigma = np.std(inter_event_times)
beta = tau_var/tau_mean
th_gamma_fraction = tau_mean/beta



x_values =  np.logspace(np.log10(min(inter_event_times)), np.log10(max(inter_event_times)), 300)
# # Fit the gamma distribution to the data
shape, loc, scale = gamma.fit(inter_event_times,floc=0)  # fixing loc to 0 for simplicity

beta_scipy = scale
mu_inter_event = tau_mean/beta_scipy   # 1/beta is the background rate 
gamma_fraction =  mu_inter_event #* 100 # 1/beta is the background rate 
gamma_pdf_fit = gamma.pdf(x_values, shape, loc, scale)
gamma_bg_rate = gamma_fraction*seismicity_rate_per_year

markers, stems, baseline = ax3.stem(df['datetime'], df['magnitude'],linefmt='--', 
    markerfmt='o',
      bottom = f_Mc,basefmt='-',
  )
df['mag_5s'] = df['magnitude'].apply(lambda x: "yes" if x>=5 else "no")
big_events = df.loc[df['mag_5s'] == 'yes']
plt.setp(baseline, visible=False)
plt.setp(stems, linewidth=0.5, alpha=0.5, color = 'gray')
plt.setp(markers, markersize=3,markerfacecolor='white', markeredgecolor = 'gray', alpha=0.6)

markers2, stems2, baseline2 = ax3.stem(big_events['datetime'], big_events['magnitude'],linefmt='--', 
    markerfmt='*',
      bottom = f_Mc,basefmt='-',
  )
plt.setp(baseline2, visible=False)
plt.setp(stems2, linewidth=0.8, alpha=0.8, color = 'black')
plt.setp(markers2, markersize=6,markerfacecolor='white', markeredgecolor = 'black', alpha=0.8)



ax1.plot(df['datetime'], df['index'],'.',linewidth=0.1,alpha=0.4, color='black', #colors[i],
            label="Full Catalog")

   
hist, bin_edges = np.histogram(inter_event_times, bins=x_values, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
#==== comment out to run all files
  
#===================================================================================
#============== read the NN declustered catalog file of the master catalog =========
#===================================================================================
declust_folder = f"{main_dir}/{declustered_in}"
declust_file = file.replace( '.csv', '_NN.txt')
df_NN = pd.read_csv(f"{declust_folder}/{declust_file}")
#df_NN = df_NN[df_NN['year']<2018]
df_NN['datetime'] = pd.to_datetime(df_NN[['year', 'month', 'day', 'hour', 'minute']])
 # Add the fractional seconds to the datetime column
df_NN['datetime'] = df_NN['datetime'] + pd.to_timedelta(df_NN['sec'], unit='s')
df_NN = df_NN.sort_values(by='datetime')
# Convert datetime to a numerical format (e.g., years)
df_NN['decimalyear'] = df_NN['datetime'].dt.year + df_NN['datetime'].dt.dayofyear / 365.25
df_NN = df_NN[df_NN['mag']>=f_Mc]
df_NN = df_NN.reset_index(inplace=False, drop = False)
df_NN['index'] = df_NN.index +1
#ax1.plot(df_NN['datetime'], df_NN.index, '+',linewidth=0.1,alpha=0.1, color=colors[i], )

nn_seismicity_rate_per_year = df_NN.groupby('year').size()
nn_frac = nn_seismicity_rate_per_year/seismicity_rate_per_year
nn_bg_rate = nn_frac*seismicity_rate_per_year
#bg_eq_rate_year_NN =  len(df_NN) / T_years
#bg_eq_rate_year_NN = np.mean(nn_bg_rate)

#===================================================================================
#============== read the R85 declustered catalog file of the master catalog =========
#===================================================================================

r85_folder = f"{main_dir}/{r85_in}"
r85_file = file.replace( '.csv', '_r85.csv')
df_r85 = pd.read_csv(f"{r85_folder}/{r85_file}")
#df_r85 = df_r85[df_r85['year']<2018]
df_r85['datetime'] = pd.to_datetime(df_r85[['year', 'month', 'day', 'hour', 'minute']])
 # Add the fractional seconds to the datetime column
df_r85['datetime'] = df_r85['datetime'] + pd.to_timedelta(df_r85['sec'], unit='s')
df_r85 = df_r85.sort_values(by='datetime')
df_r85['decimalyear'] = df_r85['datetime'].dt.year + df_r85['datetime'].dt.dayofyear / 365.25
df_r85 = df_r85[df_r85['magnitude']>=f_Mc]
df_r85 = df_r85.reset_index(inplace=False, drop = False)
df_r85['index'] = df_r85.index +1




r85_seismicity_rate_per_year = df_r85.groupby('year').size()
r85_frac = r85_seismicity_rate_per_year/seismicity_rate_per_year
r85_bg_rate = r85_frac*seismicity_rate_per_year  



ax1.plot(df_NN['datetime'], df_NN['index'], '.',linewidth=0.1,alpha=0.5, color='b',
              #label = f'μ_NN: {bg_eq_rate_year_NN:.0f} ev/yr'
              label = 'NN Background Events' , 
              )
ax1.plot(df_r85['datetime'], df_r85['index'], '.',linewidth=0.1,alpha=0.5,color='r',
              #label = f'μ_R85: {bg_eq_rate_year_r85:.0f} ev/yr'
              label = 'R85 Background Events',)

#==== comment out to run all files


r85_seismicity_rate_per_year = df_r85.groupby('year').size()
r85_frac = r85_seismicity_rate_per_year/seismicity_rate_per_year
r85_bg_rate = r85_frac*seismicity_rate_per_year

nn_seismicity_rate_per_year = df_NN.groupby('year').size()
nn_frac = nn_seismicity_rate_per_year/seismicity_rate_per_year
nn_bg_rate = nn_frac*seismicity_rate_per_year


df2 = pd.DataFrame()    
df2['given_year'] = seismicity_rate_per_year.index
df2['year'] = pd.to_datetime(df2['given_year'].astype(int), format='%Y')
# Apply the function to the Age column using the apply() function
df2['given_rate'] = nn_bg_rate.values
df2['Gamma'] =  gamma_bg_rate.values
df2['NN'] =  nn_bg_rate.values
df2['R85'] =  r85_bg_rate.values
   

col_name = 1
rate_dict["Gamma"][col_name] = np.array(gamma_bg_rate.values)
rate_dict["NN"][col_name] = np.array(nn_bg_rate.values)
rate_dict["R85"][col_name] = np.array(r85_bg_rate.values)



ax4.plot(df2['year'] + pd.DateOffset(months=6), df2['R85'], marker='o', linestyle='--',lw=2, color='r',markersize = 4,markerfacecolor='none',
          label="R85 Rate" )
ax4.plot(df2['year'] + pd.DateOffset(months=6), df2['NN'], marker='s', linestyle='--',lw=2, color='b',markersize=4,markerfacecolor='none',
          label="NN Rate"   )
ax4.plot(df2['year'] + pd.DateOffset(months=6),df2['Gamma'], marker='d', linestyle='--',lw=3, color='white',markersize=5,markerfacecolor='none',
          label="Gamma Rate"   )
ax4.plot(df2['year'] + pd.DateOffset(months=6),df2['Gamma'], marker='d', linestyle='--',lw=2, color='green',markersize=4,markerfacecolor='none',
          label="Gamma Rate"   )

ax1.set_ylim([0,55000])
ax1.set_ylabel('Cumulative No of Events',  fontsize = 16, font = "Times New Roman")

ax3.set_xlabel('Time',  fontsize = 16, font = "Times New Roman")
ax3.set_ylabel('Magnitude',  fontsize = 16, font = "Times New Roman")
ax3.set_ylim([2.5,9])

ax4.set_ylabel('Background Rate [ev/yr]')

axs=[ax1,ax3,ax4]
for ax in axs:
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))  # Use dictionary to remove duplicates
    ax.legend(unique_labels.values(), unique_labels.keys(), loc='upper left')

    # Set tick parameters
    if ax == ax4:
        pass
    else:

        minor_y = plt.MultipleLocator(10)  
        ax.yaxis.set_minor_locator(minor_y)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_major_locator(mdates.YearLocator(5))  # Major ticks every 5 years
        #ax.xaxis.set_minor_locator(mdates.YearLocator(1))  # Minor ticks every year
        #ax.xaxis.set_minor_locator(AutoMinorLocator(10))
        ax.minorticks_on() 

        ax.tick_params(axis='both', colors='black', right=False, top=False, **minorTick)
        ax.tick_params(axis='both', colors='black', right=False, top=False, **majorTick)
        ax.grid(visible=True, which='major', linestyle='--', color='gray', alpha=0.5)
        ax.grid(visible=True, which='minor', linestyle='--', color='gray', alpha=0.2)
        
        ax.spines['left'].set_color('black')
        ax.spines['right'].set_color('black')
        
#Add annotations dynamically from the file
annotations = pd.read_csv(f"{code_dir}/annotations_HV.txt")
for _, row in annotations.iterrows():
    event_date = row['Datetime']  # Assuming events are marked at Jan 1 of the year
    closest_event = df[df["datetime"]== event_date]
    event_idx = closest_event.iloc[0]["index"]  
    ev_date = closest_event.iloc[0]["datetime"]  

    # Place text beside the arrow
    if event_idx < 20000:
        ax1.annotate("↓", xy=(ev_date,event_idx), xytext=(ev_date, event_idx + 4000),
                    #arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
                    ha="center", va="center")
        ax1.text(ev_date, event_idx + 7000, row["Description"], fontsize=14, color="black", rotation=90)
    else:
        ax1.annotate(" ", xy=(ev_date,event_idx), xytext=(ev_date, event_idx - 2500),
                    #arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
                    ha="center", va="center")
        
        ax1.text(ev_date, event_idx + 2000, row["Description"], fontsize=14, color="black", rotation=90)

labels = ['(a)', '(b)']

# Loop through each subplot
axes = [ax1,ax3]
for ax, label in zip(axes, labels):
    ax.text(-0.05, 0.0, label, transform=ax.transAxes, 
            fontsize=30, va='center', ha='right')
       

plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.95, wspace=0.25, hspace=0.3)
plt.show()
plt.savefig('%s/fig_HV_rate_compare.svg'%(plot_dir),dpi = 1000, transparent = True)
#

