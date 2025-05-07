#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 09:47:08 2025

@author: rinty
"""

def dateTime2decYr( datetime_in, **kwargs ):
    """
    input: datetime_in = array containing time columns year - second
                   out = date in decimal year
                   
    """
    import datetime
    import calendar
    try:
        o_dt = datetime.datetime( int( datetime_in[0] ), int( datetime_in[1] ), int( datetime_in[2] ), int( datetime_in[3] ), int( datetime_in[4] ), int( round( datetime_in[5])))
    except:
        error_msg = "datetime array not valid - %s; check if date and time is correct, e.g. no SC > 60.." % datetime_in
        raise( ValueError( error_msg))
    time_sc = o_dt.hour*3600 + o_dt.minute*60 + o_dt.second    
    # get no. of day within current year between 0 to 364 and ad time in seconds
    dayOfYear_seconds = ( o_dt.timetuple().tm_yday - 1 ) * 86400.0 + time_sc
    if calendar.isleap( o_dt.year):
        year_fraction = dayOfYear_seconds / ( 86400.0 * 366 )
    else:
        year_fraction = dayOfYear_seconds / ( 86400.0 * 365 )
    # dec year = current year + day_time (in dec year)
    return o_dt.year + year_fraction



import numpy as np

#===================================================================================
#                         rate computation
#===================================================================================
def eqRate( at, k_win):
    # smoothed rate from overlapping sample windows normalized by delta_t
    aS          = np.arange( 0, at.shape[0]-k_win, 1)
    aBin, aRate = np.zeros(aS.shape[0]), np.zeros(aS.shape[0])
    iS = 0
    for s in aS:
        i1, i2 = s, s+k_win
        aBin[iS]  = 0.5*( at.iloc[i1]+at.iloc[i2])
        aRate[iS] = k_win/( at.iloc[i2]-at.iloc[i1])
        iS += 1
    return aBin, aRate

import os
import json
def update_config(params, inp, i):
    config_path = os.path.dirname(os.getcwd())
    config_in = os.path.join(config_path,'config')#f"{os.environ['HOME']}/Desktop/Research/ETAS/etas-main/config/"
    os.chdir(config_in)
    y1,y2,mu_value, a, omega,rho, log_c, d, gamma, tau, k0 = params
    shape_file, cat_type, rate_type = inp
    config_file = "simulate_catalog_config_%s.json"%cat_type

    with open(config_file, "r") as file:
        config_data = json.load(file)

    # Update parameters in config
    config_data["fn_store"] = "../output_data/%s/simulated_%s_catalog%i.csv"%(rate_type,cat_type,i)
    config_data["shape_coords"]= "../input_data/%s"%shape_file
    config_data["primary_start"] = y1
    config_data["end"] = y2
    config_data["parameters"]["log10_mu"] = mu_value #np.log10(5.5e-7)  # Fix background rate    
    config_data["parameters"]["log10_k0"] = k0
    config_data["parameters"]["a"] = a
    config_data["parameters"]["log10_c"] = log_c
    config_data["parameters"]["omega"] = omega
    config_data["parameters"]["log10_tau"] = tau
    config_data["parameters"]["log10_d"] = d
    config_data["parameters"]["gamma"] = gamma
    config_data["parameters"]["rho"] = rho

    # Save updated config
    with open(config_file, "w") as file:
        json.dump(config_data, file, indent=4)


from datetime import datetime, timedelta
def decimal_year_to_datetime(decimal_year):
    year = int(decimal_year)
    days_in_year = 366 if datetime(year, 12, 31).timetuple().tm_yday == 366 else 365
    result_date = datetime(year, 1, 1) + timedelta(days=(decimal_year - year) * days_in_year)
    return result_date


