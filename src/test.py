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

#%%
a1 = np.array(df['NSS Overall (%)'])
a2 = np.array(df['Student:staff ratio'])
corr_nssoverall_ssratio = np.corrcoef(a1, a2)

a3 = np.array(df['NSS Feedback (%)'])
corr_nssfb_ssratio = np.corrcoef(a3, a2)


a4 = np.array(df['NSS Teaching (%)'])
corr_nssteaching_ssratio = np.corrcoef(a4, a2)

a5 = np.array(df['Value added score/10'])
a6 = np.array(df['Career prospects (%)'])
a7 = np.array(df['Entry Tariff'])
a8 = np.array(df['Expenditure per student / 10'])
corr_value_career = np.corrcoef(a5, a6)

corr_teaching_overall = np.corrcoef(a1,a4)
corr_feedback_overall = np.corrcoef(a1,a3)
corr_tariff_value = np.corrcoef(a7,a5)
corr_spend_ratio = np.corrcoef(a8,a2)
#%%
df_temp = df.iloc[:,5:14]
df_corr = df_temp.corr()
#%% prediction


aa = np.array(df['NSS Overall (%)'])
