# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 18:39:37 2024

@author: yuziq
"""

import os
import math
import copy
import pandas as pd
import PySimpleGUI as sg
import lib_extract_data as led
from matplotlib import pyplot as plt 

file = os.path.abspath('../data/TheGuardianRanking.xlsx')
df = led.read_data_from_file(file)
fields,df_dict_in_year,df_dict_in_institution = led.update_df(df)


values = df.values.tolist()
sg.theme("DarkBlue3")
sg.set_options(font=("Courier New", 12))

layout = [[sg.Table(values = values, headings = fields,
    # Set column widths for empty record of table
    auto_size_columns=True,
    col_widths=list(map(lambda x:len(x)+1, fields)))]]

window = sg.Window('Sample excel file',  layout)
while True:
    event, values = window.read()