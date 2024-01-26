# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 20:53:40 2024

@author: ziqing
"""
import os
import math
import copy
import lib_extract_data as led

file = os.path.abspath('../data/TheGuardianRanking.xlsx')
df = led.read_data_from_file(file)

# divide data into year class
df_dict_in_year = {}
years =   df['Ranking Year'].unique()
for item in years:
    df_temp = df[df['Ranking Year'] == item]
    df_dict_in_year[item] = df_temp.reindex()

fields = list(df.columns.values)

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