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

#%%

    
#%% select elements
lst_year = sg.Combo(list(df_dict_in_year.keys()), \
                    expand_x=True, enable_events=True, key='Ranking Year')
layout_table = [[sg.Text('Ranking Year:'),lst_year],
                [sg.Text('  ')]]
table_type_dict = led.row_type_for_table(df, fields)

for item in fields:
    if not (item == 'Ranking Year'):
        if table_type_dict[item]['type'] == 'range':
            vmin = table_type_dict[item]['min']
            vmax = table_type_dict[item]['max']
            layout_table.append([sg.Text(item),\
                                 sg.Text(f'Min (from {vmin})'),\
                                     sg.Input(key=f'min_{item}'),\
                                 sg.Text(f'Max (to {vmax})'),\
                                     sg.Input(key=f'max_{item}'),])
        '''elif table_type_dict[item]['type'] == 'multiselect':
            names = table_type_dict[item]['values']
            layout_table.append([sg.Text(item),sg.Listbox(names, \
                        expand_y=True, enable_events=True, key=f'list_{item}')])'''
layout_table.append([sg.Button('OK'),sg.Button('Cancel')])
window = sg.Window('UK Uni Case Study', layout_table)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    elif event == 'OK':
        # generate the table
        pass
window.close()
#%% generate table according to the values
condition = led.filter_choose(df,'Ranking Year',[values['Ranking Year']])
for item in table_type_dict:
    if item == 'Ranking Year':
        continue
    elif table_type_dict[item]['type'] == 'range':
        if values[f'min_{item}'] == '':
            rmin = table_type_dict[item]['min']
        else:
            rmin = float(values[f'min_{item}'])
        if values[f'max_{item}'] == '':
            rmax = table_type_dict[item]['max']
        else:
            rmax = float(values[f'max_{item}'])
        condition_temp = led.filter_range(df, item, rmin, rmax)
        condition = condition & condition_temp

df_present = df.loc[condition,:]
values = df_present.values.tolist()
sg.theme("DarkBlue3")
sg.set_options(font=("Courier New", 12))

layout = [[sg.Table(values = values, headings = fields,
    # Set column widths for empty record of table
    auto_size_columns=True,
    col_widths=list(map(lambda x:len(x)+1, fields)))]]

window = sg.Window('Sample excel file',  layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
window.close()

#%% select institutions to draw the trends
fields_plot = copy.deepcopy(fields)
fields_plot.remove('Ranking Year')
fields_plot.remove('Institution')
layout_trend = [[sg.Text('Select the Institutions'),\
                 sg.Listbox(list(df_dict_in_institution.keys()), \
                 size=(20, 5),expand_y=True, enable_events=True, key='institution')],\
                [sg.Text('Select the factors'),sg.Listbox(fields_plot, \
                 size=(20, 5),expand_y=True, enable_events=True, key='factors')],
                [sg.Button('OK'),sg.Button('Cancel')]]
window = sg.Window('Trend',  layout_trend)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    else:
        time_plot = []
        fields_chosen = values['factors']
        fig,ax = plt.subplots()
        for i,item1 in enumerate(fields_chosen):
            for j,item2 in enumerate(values['institution']):     
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
            ax.legend(values['institution'])
            fig.show()
window.close()   
    
#%% 
