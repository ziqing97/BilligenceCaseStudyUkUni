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



#%% prediction

