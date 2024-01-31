# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 20:53:40 2024

@author: ziqing
"""

import os
from datetime import datetime,date
import math
import copy
import pandas as pd
import PySimpleGUI as sg
import numpy as np
import lib_extract_data as led
from matplotlib import pyplot as plt 

file = os.path.abspath('../data/TheGuardianRanking.xlsx')
df = led.read_data_from_file(file)
fields,df_dict_in_year,df_dict_in_institution = led.update_df(df)

#%% check result
for ins in df_dict_in_institution.keys():
    df = df_dict_in_institution[ins]
    df = df.sort_values(by='Ranking Year')
    rprev = list(df['Ranking (Prev)'])
    rnow = list(df['Ranking'])
    for i in range(0,len(rnow)-1):
        if rnow[i] == rprev[i+1]:
            continue
        else:
            print(f'{ins}')

#%% translate ratio to 100 punkten
df = df_dict_in_year[2015]
ratio_max = df['Student:staff ratio'].max()
ration_min = df['Student:staff ratio'].min()
scale_ratio = (ratio_max-ration_min)/10
tariff_max = df['Entry Tariff'].max()
tariff_min = df['Entry Tariff'].min()
scale_tariff = (tariff_max-tariff_min)/10

for item in df.index:
    ratio = df.loc[item,'Student:staff ratio']
    df.loc[item,'s:s points'] = (ratio_max - ratio)/scale_ratio*10
    df.loc[item,'Expenditure points'] = df.loc[item,'Expenditure per student / 10']*10
    df.loc[item,'Value points'] = df.loc[item,'Value added score/10']*10
    tariff = df.loc[item,'Entry Tariff']
    df.loc[item,'tariff points'] = (tariff-tariff_min)/scale_tariff*10

#%%
df['Calculated Score'] = df['NSS Teaching (%)']*0.1 + \
                         df['NSS Feedback (%)'] * 0.1 +\
                        df['NSS Overall (%)']*0.05 + df['Value points']*0.15 + \
                            df['s:s points']*0.15 + df['Expenditure points']*0.15 +\
                            df['tariff points'] *0.15 + df['Career prospects (%)']*0.15

df2 = df[['Guardian score/100','Calculated Score']]
#%% prediction

