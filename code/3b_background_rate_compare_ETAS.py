#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 13:01:31 2025

@author: rinty
"""


import numpy as np
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
from scipy import stats
from scipy.stats import gaussian_kde, kstest, gamma
from scipy.stats import variation
from scipy.optimize import curve_fit

#project_dir = os.getcwd()
project_dir = os.getcwd()
main_dir = os.path.dirname(project_dir)
os.chdir(main_dir)

code_dir = os.path.join(main_dir,'code')
os.chdir(code_dir)
import define_rates as rate
#from utils import decimal_year_to_datetime
#__**__Make sure to change  the rate based on catalog types
rate1 = rate.stable_rate
rate2 = rate.int_rate
rate3 = rate.short_rate


plot_dir = os.path.join(main_dir, 'plots')
type_1 = 'HV_stable_rate'
type_2 = 'HV_intermediate_rate'
type_3 = 'HV_short_term_rate'
cat_type = type_1
file = 'synthetic_stable_rate1.csv'

if cat_type == type_1:
    word = 'rate'
    dir_in = 'data'
    declustered_in = 'data_processed/declustered' 
    r85_in = 'r85'
    c = 'green'    
    #file = 'synthetic_stable_rate5.csv'
    outfile = 'syn_HV_rate_compare_stable'
if cat_type == type_2:
    c = 'red'
    word = 'rate'
    dir_in = 'data'
    declustered_in = 'data_processed/declustered' 
    r85_in = 'r85'
    #file = 'synthetic_intermediate_rate2.csv'
    outfile = 'syn_HV_rate_compare_intermediate'
    
if cat_type == type_3:
    c = 'blue'
    word = 'rate'
    dir_in = 'data'
    declustered_in = 'data_processed/declustered' 
    r85_in = 'r85'
    #file = 'synthetic_short_term_rate8.csv'
    outfile = 'syn_HV_rate_compare_short_term'
    
os.chdir(f"{main_dir}/{dir_in}")

r85 = False

fig = plt.figure(figsize=(14,8))
gs = fig.add_gridspec(2, 2)

ax1 = fig.add_subplot(gs[0, :])
ax3 = fig.add_subplot(gs[1, :]) 
ax4 = ax3.twinx()



plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize']=14
plt.rcParams['ytick.labelsize']=14
plt.rcParams['axes.labelsize']=14
minorTick = {'which': 'minor', 'direction': 'out', 'length': 4, 'width': 0.5}
majorTick = {'which': 'major', 'direction': 'out', 'length': 8, 'width': 1}


approaches = ["Gamma", "NN", "R85"]

if cat_type[0:2] == 'HV':   
    years = np.arange(1959,2025)
else:
    years = np.arange(1981,2025)
error_dict = {approach: pd.DataFrame(index=years) for approach in approaches}
rate_dict = {approach: pd.DataFrame(index=years) for approach in approaches}

f_Mc = 2.5

catalog_name = file[:-4]
print(catalog_name)
df_master = pd.read_csv(f"{main_dir}/{dir_in}/{file}")

df = df_master
df ['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
#Add the fractional seconds to the datetime column
df['datetime'] = df['datetime'] + pd.to_timedelta(df['sec'], unit='s')
df = df.sort_values(by='datetime') 
df = df[df['magnitude']>=f_Mc]
df.reset_index(inplace=True, drop=True)
df['index'] = df.index+1

df['inter_event_time'] = df['datetime'].diff().dt.total_seconds()/ (24 * 3600)
#x = np.array([t.timestamp() for t in df['datetime']])

df['decimalyear'] = df['datetime'].dt.year + df['datetime'].dt.dayofyear / 365.25

# Drop the first NaN value resulting from the diff operation
df = df.dropna(subset=['inter_event_time'])
    
N = len(df)
T_days = (df['datetime'].max()- df['datetime'].min()).days
T_years = (df['datetime'].max().year- df['datetime'].min().year)

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
# scale = beta_scipy
# shape = lambda_scipy
beta_scipy = scale
mu_inter_event = tau_mean/beta_scipy   # 1/beta is the background rate 
gamma_fraction =  mu_inter_event #* 100 # 1/beta is the background rate 
gamma_pdf_fit = gamma.pdf(x_values, shape, loc, scale)
gamma_bg_rate = gamma_fraction*seismicity_rate_per_year
#gamma_rate = np.mean(gamma_bg_rate)
#gamma_rate = gamma_fraction*total_eq_rate_year


#============ only true backgrund events========
bg_file = file.replace( '.csv', '_bg.txt')
df_bg = pd.read_csv(f"{main_dir}/{dir_in}/{bg_file}")
df_bg ['datetime'] = pd.to_datetime(df_bg[['year', 'month', 'day', 'hour', 'minute']])
df_bg['datetime'] = df_bg['datetime'] + pd.to_timedelta(df_bg['sec'], unit='s')
df_bg = df_bg.sort_values(by='datetime') 
df_bg = df_bg[df_bg['magnitude']>=f_Mc]
df_bg.reset_index(inplace=True, drop=True)
df_bg['index'] = df_bg.index+1


# #==== comment out to run all files
markers, stems, baseline = ax3.stem(df['datetime'], df['magnitude'],linefmt='--', 
    markerfmt='o',
      bottom = f_Mc,basefmt='-',
  )
df['mag_5s'] = df['magnitude'].apply(lambda x: "yes" if x>=5 else "no")
big_events = df.loc[df['mag_5s'] == 'yes']
plt.setp(baseline, visible=False)
#plt.setp(baseline, visible=False)
plt.setp(stems, linewidth=0.5, alpha=0.5, color = 'gray')
plt.setp(markers, markersize=3,markerfacecolor='white', markeredgecolor = 'gray', alpha=0.6)

markers2, stems2, baseline2 = ax3.stem(big_events['datetime'], big_events['magnitude'],linefmt='--', 
    markerfmt='*',
      bottom = f_Mc,basefmt='-',
  )
plt.setp(baseline2, visible=False)
plt.setp(stems2, linewidth=0.8, alpha=0.8, color = 'black')
plt.setp(markers2, markersize=7,markerfacecolor='white', markeredgecolor = 'black', alpha=0.8)


ax1.plot(df['datetime'], df['index'],'.',linewidth=0.1,alpha=0.4, color='black', #colors[i],
            label="Full Catalog")
ax1.plot(df_bg['datetime'], df_bg['index'],'.',linewidth=0.1,alpha=0.5, color='orange', #colors[i],
            label="True Background Events")
   
hist, bin_edges = np.histogram(inter_event_times, bins=x_values, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
#==== comment out to run all files


    
#===================================================================================
#============== read the NN declustered catalog file of the master catalog =========
#===================================================================================
declust_folder = f"{main_dir}/{declustered_in}"
if cat_type[0:2]== 'HV':
    declust_file = file.replace( '.csv', '_NN.txt')
else:
    declust_file = file.replace( '.csv', '_NN_d1.6.txt')
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
if r85 == True:
    r85_folder = f"{main_dir}/r85/synthetic/{r85_in}"
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
    #bg_eq_rate_year_r85 =  len(df_r85) / T_years
    #bg_eq_rate_year_r85 = np.mean(r85_bg_rate)


    ax1.plot(df_r85['datetime'], df_r85['index'], '.',linewidth=0.1,alpha=0.5,color='r',
              #label = f'μ_R85: {bg_eq_rate_year_r85:.0f} ev/yr'
              label = 'R85 Background Events',)

    r85_seismicity_rate_per_year = df_r85.groupby('year').size()
    r85_frac = r85_seismicity_rate_per_year/seismicity_rate_per_year
    r85_bg_rate = r85_frac*seismicity_rate_per_year



ax1.plot(df_NN['datetime'], df_NN['index'], '.',linewidth=0.1,alpha=0.5, color='b',
              #label = f'μ_NN: {bg_eq_rate_year_NN:.0f} ev/yr'
              label = 'NN Background Events' , 
              )

nn_seismicity_rate_per_year = df_NN.groupby('year').size()
nn_frac = nn_seismicity_rate_per_year/seismicity_rate_per_year
nn_bg_rate = nn_frac*seismicity_rate_per_year


if cat_type == type_2:  
    rate = rate2
elif cat_type == type_3:  
        rate = rate3
else:
    rate = rate1
    
df2 = pd.DataFrame()    
df2['given_year'] = seismicity_rate_per_year.index
df2['year'] = pd.to_datetime(df2['given_year'].astype(int), format='%Y')
# Apply the function to the year column using the apply() function
df2['given_rate'] = df2['given_year'].apply(rate)
df2['Gamma'] =  gamma_bg_rate.values
df2['NN'] =  nn_bg_rate.values

 

col_name = 1
rate_dict["Gamma"][col_name] = np.array(gamma_bg_rate.values)
rate_dict["NN"][col_name] = np.array(nn_bg_rate.values)
  
col_name = 1
error_dict["Gamma"][col_name] = np.array(((df2.given_rate -   gamma_bg_rate.values))/df2.given_rate)
error_dict["NN"][col_name] = np.array(((df2.given_rate -   nn_bg_rate.values))/df2.given_rate)

    

# #==== comment out to run all files


median_gamma_rate = rate_dict['Gamma'].median(axis=1)
median_nn_rate = rate_dict['NN'].median(axis=1)
   


ax4.plot(df2['year']+ pd.DateOffset(months=6), df2['given_rate'].values, marker='x', linestyle='-',lw=3, color='black',markersize=4,markerfacecolor='none',
              label="Given Rate"  )    

ax4.plot(df2['year']+ pd.DateOffset(months=6), median_nn_rate.values, marker='s', linestyle='--',lw=2, color='b',markersize=4,markerfacecolor='none',
          label="NN Rate"  )
ax4.plot(df2['year']+ pd.DateOffset(months=6), median_gamma_rate.values, marker='d', linestyle='--',lw=2, color='green',markersize=4,markerfacecolor='none',
          label="Gamma Rate"  )

if r85 == True: 
    df2['R85'] =  r85_bg_rate.values
    rate_dict["R85"][col_name] = np.array(r85_bg_rate.values)
    error_dict["R85"][col_name] = np.array(((df2.given_rate -   r85_bg_rate.values))/df2.given_rate)
    median_r85_rate = rate_dict['R85'].median(axis=1)

    ax4.plot(df2['year']+ pd.DateOffset(months=6), median_r85_rate.values, marker='o', linestyle='--',lw=2, color='r',markersize = 4,markerfacecolor='none',
          label="R85 Rate"  )     


    
median_gamma_error = error_dict['Gamma'].median(axis=1)
median_nn_error = error_dict['NN'].median(axis=1)




ax1.xaxis.set_major_locator(mdates.YearLocator(10))
ax1.xaxis.set_minor_locator(mdates.YearLocator(1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
#ax1.legend(loc='upper left',fontsize=8)
xlim = ax1.get_xlim()
ylim = ax1.get_ylim()
#ax1.set_xlabel('Time')
ax1.set_ylabel('Cumulative No of Events', fontsize = 16, font = "Times New Roman")
#ax1.set_title('Cumulative Events')#' with Background Rate %s'%given_rate1)
#ax1.grid(True)


#ax3.set_xlabel('Time')
ax3.set_ylabel('Magnitude', fontsize = 16, font = "Times New Roman")
ax3.set_ylim([int(f_Mc),9])
ax3.set_xlabel('Time', fontsize = 16, font = "Times New Roman")
#ax4.legend(loc='upper left', fontsize = 7)
#ax4.grid()
ax4.set_ylabel('Background Rate [ev/yr]')

# Remove duplicate legends
axs=[ax1,ax3,ax4]
for ax in axs:
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))  # Use dictionary to remove duplicates
    ax.legend(unique_labels.values(), unique_labels.keys(), loc='upper left')

    # Set tick parameters
    if ax == ax4:
        pass
    else:

        ax.xaxis.set_major_locator(mdates.YearLocator(10))
        ax.xaxis.set_minor_locator(mdates.YearLocator(1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.tick_params(axis='both', colors='black', right=False, top=False, **minorTick)
        ax.tick_params(axis='both', colors='black', right=False, top=False, **majorTick)
        ax.grid(visible=True, which='major', linestyle='--', color='gray', alpha=0.5)
        ax.grid(visible=True, which='minor', linestyle='--', color='gray', alpha=0.2)
        
        ax.spines['left'].set_color('black')
        ax.spines['right'].set_color('black')


plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.95, wspace=0.25, hspace=0.3)
plt.show()
plt.savefig( '%s/fig_%s.svg'%(plot_dir, outfile),dpi = 500, transparent = True)

