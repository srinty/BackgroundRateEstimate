#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 13:04:55 2025

@author: rinty
"""
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def decimal_year_to_datetime(decimal_year):
    year = int(decimal_year)
    days_in_year = 366 if datetime(year, 12, 31).timetuple().tm_yday == 366 else 365
    result_date = datetime(year, 1, 1) + timedelta(days=(decimal_year - year) * days_in_year)
    return result_date


def plot_style(ax):
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 12
    #font = {'family': 'Times New Roman', 'weight': 'bold', 'size': 16}
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['xtick.labelsize']=12
    plt.rcParams['ytick.labelsize']=12
    plt.rcParams['axes.labelsize']=12

    minorTick = {'which': 'minor', 'direction': 'out', 'length': 4, 'width': 0.5}
    majorTick = {'which': 'major', 'direction': 'out', 'length': 8, 'width': 1}
    minor_x = plt.MultipleLocator(2)  
    ax.xaxis.set_minor_locator(minor_x)
    minor_y = plt.MultipleLocator(10)  
    ax.yaxis.set_minor_locator(minor_y)

    # Set tick parameters
    ax.minorticks_on()
    ax.tick_params(axis='both', colors='black', right=False, top=False, **minorTick)
    ax.tick_params(axis='both', colors='black', right=False, top=False, **majorTick)
    ax.grid(visible=True, which='major', linestyle='--', color='gray', alpha=0.5)
    ax.grid(visible=True, which='minor', linestyle='--', color='gray', alpha=0.2)
    
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    
    
    
    
    
    
    
    