#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 12:19:40 2024

@author: rinty
"""
def stable_rate(year):
    #if year >=1959 and year<=2025:
        return 80
    
def stable_rate2(year):
        return 50

    
def int_rate(year):
    if year < 1981:
        return 60
    if year >= 1981 and year < 2003:
         return 100
    if year >= 2003 and year < 2025:
        return 80

def int_rate2(year):
    if year < 1981:
        return 20
    if year >= 1981 and year < 2003:
         return 40
    if year >= 2003 and year < 2025:
        return 30

def short_rate(year):
    if year < 1965:
        return 60
    if year >= 1965 and year <1970:
         return 80
    if year >= 1970 and year <1975:
        return 60
    if year >= 1975 and year <1980:
        return 80
    if year >= 1980 and year <1985:
        return 100
    if year >= 1985 and year <1990:
         return 80
    if year >= 1990 and year <1995:
        return 60
    if year >= 1995 and year <2000:
        return 80
    if year >= 2000 and year <2005:
        return 100
    if year >= 2005 and year <2010:
        return 80
    if year >= 2010 and year <2015:
        return 60
    if year >= 2015 and year <2020:
        return 80
    if year >= 2020 and year <2025:
        return 60
    
def short_rate2(year):
    if year < 1965:
        return 20
    if year >= 1965 and year <1970:
         return 40
    if year >= 1970 and year <1975:
        return 20
    if year >= 1975 and year <1980:
        return 40
    if year >= 1980 and year <1985:
        return 60
    if year >= 1985 and year <1990:
         return 40
    if year >= 1990 and year <1995:
        return 20
    if year >= 1995 and year <2000:
        return 40
    if year >= 2000 and year <2005:
        return 60
    if year >= 2005 and year <2010:
        return 40
    if year >= 2010 and year <2015:
        return 20
    if year >= 2015 and year <2020:
        return 40
    if year >= 2020 and year <2025:
        return 20
    
    
def SC_stable_rate(year):
    #if year >=1980 and year<=2025:
        return 60
    
def SC_int_rate(year):
    if year < 1995:
        return 60
    if year >= 1995 and year < 2010:
         return 100
    if year >= 2010 and year < 2025:
        return 80
    
def SC_int_rate(year):
    if year < 1995:
        return 20
    if year >= 1995 and year < 2010:
         return 40
    if year >= 2010 and year < 2025:
        return 30