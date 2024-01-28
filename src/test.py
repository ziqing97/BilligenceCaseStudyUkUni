# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 20:53:40 2024

@author: ziqing
"""
import os
import math
import copy
import pandas as pd
import numpy as np
import lib_extract_data as led
from matplotlib import pyplot as plt 

#%%
file = os.path.abspath('../data/TheGuardianRanking.xlsx')
df = led.read_data_from_file(file)

#%% divide data into year class
fields,df_dict_in_year,df_dict_in_institution = led.update_df(df)
# function range test
vmin = 400
vmax = 600
df_year = df_dict_in_year[2015]
field = fields[12]
condition = led.filter_range(df_year, field, vmin, vmax)
df_condition = df_year.loc[condition,:]

# function choose test
chosen_list = ['Aberdeen']
condition = led.filter_choose(df, field, chosen_list)
df_condition = df_year.loc[condition,:]

#%% function trend
fields_chosen = ['Ranking','Value added score/10','Student:staff ratio']
institutions_chosen = ['Aberdeen','UC Suffolk','Cambridge','Buckingham']

fig,ax = plt.subplots(len(fields_chosen))
time_plot = []
for i,item1 in enumerate(fields_chosen):
    fig,ax = plt.subplots()
    for j,item2 in enumerate(institutions_chosen):     
        data = df_dict_in_institution[item2][item1]
        time = df_dict_in_institution[item2]['Ranking Year']
        # add previous ranking into ranking
        if item1 == 'Ranking':
            data2 = df_dict_in_institution[item2]['Ranking (Prev)'].iloc[0]
            data = pd.Series([data2]+list(data))
        else:
            data = pd.Series([None]+list(data))
        time2 = time.iloc[0]-1
        time = pd.Series([time2]+list(time))
        # document time 
        if len(time_plot)<len(time):
            print(len(time))
            time_plot = time
        # plot
        ax.plot(time,data)
    ax.set_xticks(time_plot)
    ax.set_xticklabels(time_plot)
    ax.legend(institutions_chosen)


#%% prediction

#%%
def row_type_for_table(df,fields):
    type_dict = {}
    for item in fields:
        if isinstance(df.loc[0,item],np.int64) or isinstance(df.loc[0,item],float):
            type_dict[item] = {'type':'range'}
            value_min = math.ceil(df.loc[:,item].min())
            value_max = int(df.loc[:,item].max())
            type_dict[item]['min'] = value_min
            type_dict[item]['max'] = value_max
        else:
            type_dict[item] = {'type':'multiselect'}
            type_dict[item]['values'] = df[item].unique()
        return type_dict
        
        