# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 13:47:32 2024

@author: yuziq
"""
import copy
from datetime import datetime
import PySimpleGUI as sg
import pandas as pd
from matplotlib import pyplot as plt
import lib_extract_data as led
sg.theme("DarkBlue3")
sg.set_options(font=("Microsoft JhengHei", 16))
class BilligenceCaseStudy():
    '''
    Class for the whole mini project
    '''
    def __init__(self):
        self.dataframe = None
        self.fields = []
        self.df_dict_in_year = {}
        self.df_dict_in_institution = {}
        self.main()

    def main(self):
        '''
        main gui framework
        '''
        layout_load = [  [sg.Text('Functions')],
                    [sg.Button('Load data'), sg.Button('Compare data in one year'),\
                     sg.Button('Compare trend')],\
                    [sg.Button('Exit')]]

        window = sg.Window('UK Uni Case Study', layout_load)
        while True:
            event, _ = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
                break
            else:
                if event == 'Load data':
                    self.gui_read_data()
                elif event == 'Compare data in one year':
                    self.gui_table_select_view()
                elif event == 'Compare trend':
                    self.gui_trend_view()
                # load new window according to the event
        window.close()

    def gui_read_data(self):
        '''
        gui window for loading data
        '''
        layout_load = [  [sg.Text('Load the data')],
                    [sg.Text('Give the data here'),sg.Input(),sg.FileBrowse()],
                    [sg.Button('Ok'), sg.Button('Cancel')] ]

        window = sg.Window('UK Uni Case Study', layout_load)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            elif event == 'Ok':
                file = values[0]


            dataframe_temp = led.read_data_from_file(file)
            if self.dataframe is None:
                self.dataframe = dataframe_temp
            else:
                new_field = list(dataframe_temp.keys())
                for item in new_field:
                    if item == 'Ranking Year' or item == 'Institution':
                        continue
                    if item in self.dataframe.keys():
                        dataframe_temp.rename(columns={item:f'{item}_new'},\
                                              inplace=True)
                self.dataframe = pd.merge(self.dataframe,dataframe_temp,\
                                  on=['Ranking Year','Institution'],how='outer')
                # self.dataframe = led.combine_df(self.dataframe,dataframe.temp)
            self.fields,self.df_dict_in_year,self.df_dict_in_institution = \
                led.update_df(self.dataframe)
            break
        window.close()

    def gui_table_select_view(self):
        '''
        gui window for selecting table elements
        '''
        lst_year = sg.Combo(list(self.df_dict_in_year.keys()), \
                            expand_x=True, enable_events=True, key='Ranking Year',size=(4,1))
        layout_table = [[sg.Text('Ranking Year:',size=(15,1)),lst_year],
                        [sg.Text('  ')]]
        table_type_dict = led.row_type_for_table(self.dataframe, self.fields)

        for item in self.fields:
            if not item == 'Ranking Year':
                if table_type_dict[item]['type'] == 'range':
                    vmin = table_type_dict[item]['min'].round(2)
                    vmax = table_type_dict[item]['max'].round(2)
                    layout_table.append([sg.Text(f'{item}\t',size=(25,1)),\
                                         sg.Text(f'Min (from {vmin})\t'),\
                                             sg.Input(key=f'min_{item}',size=(4,1)),\
                                         sg.Text(f'Max (to {vmax})\t'),\
                                             sg.Input(key=f'max_{item}',size=(4,1)),])
        layout_table.append([sg.Button('OK'),sg.Button('Cancel')])
        window = sg.Window('UK Uni Case Study', layout_table, grab_anywhere=True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            elif event == 'OK':
                # generate the table
                self.gui_table_view(table_type_dict, values)
        window.close()

    def gui_table_view(self,table_type_dict,values):
        '''
        gui window for table presentation
        '''
        condition = led.filter_choose(self.dataframe,'Ranking Year',[values['Ranking Year']])
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
                condition_temp = led.filter_range(self.dataframe, item, rmin, rmax)
                condition = condition & condition_temp

        df_present = self.dataframe.loc[condition,:]
        df_present = df_present.round(2)
        values2 = df_present.values.tolist()
        sg.theme("DarkBlue3")
        sg.set_options(font=("Courier New", 10))
        headings = copy.deepcopy(self.fields)
        layout = [[sg.Table(values = values2, headings = headings,
            selected_row_colors='red on yellow',
            auto_size_columns=False,
            # row_height=10,
            enable_events=True,
            expand_x=True,
            expand_y=True,
            col_widths=4,
            key = 'table1')],
            [sg.Text('Sorted by'), sg.Combo(self.fields,key='sortedelement'),\
             sg.Text('Order'),sg.Combo(['Ascending','Descending'],key='order'),sg.Button('OK')],\
             [sg.Button('Export')]]
        ryear = values['Ranking Year']
        window = sg.Window(f'Filtered data on {ryear}',  layout, size=(1600, 400), resizable=True)
        while True:
            event, values_sor = window.read()
            # df_present = df_present.sort_values(by=values_sor[''],ascending=True)
            if event == sg.WIN_CLOSED:
                break
            elif event == 'OK':
                order = values_sor['order']
                if order == 'Ascending':
                    df_present = df_present.sort_values(by=values_sor['sortedelement'],\
                                                        ascending=True)
                else:
                    df_present = df_present.sort_values(by=values_sor['sortedelement'],\
                                                        ascending=False)
                values2 = df_present.values.tolist()
                window['table1'].update(values=values2)
            elif event == 'Export':
                now = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f'table_{now}.csv'
                df_present.to_csv(filename)
                continue
        window.close()

    def gui_trend_view(self):
        '''
        gui window for choosing trend plot elements
        '''
        fields_plot = copy.deepcopy(self.fields)
        fields_plot.remove('Ranking Year')
        fields_plot.remove('Institution')
        layout_trend = [[sg.Text('Select the Institutions'),\
                         sg.Listbox(list(self.df_dict_in_institution.keys()), \
                         size=(20, 10),expand_y=True, enable_events=True,\
                            select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, key='institution'),\
                        sg.Text('Select the factors'),sg.Listbox(fields_plot, \
                         size=(20, 10),expand_y=True, enable_events=True,\
                            select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, key='factors')],
                        [sg.Button('OK'),sg.Button('Cancel')]]
        window = sg.Window('Trend',  layout_trend,size=(1000, 400), resizable=True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'OK':
                time_plot = []
                fields_chosen = values['factors']
                for item1 in fields_chosen:
                    fig,ax = plt.subplots()
                    for item2 in values['institution']:
                        data = self.df_dict_in_institution[item2][item1]
                        time = self.df_dict_in_institution[item2]['Ranking Year']
                        # add previous ranking into ranking
                        if item1 == 'Ranking':
                            data2 = self.df_dict_in_institution[item2]['Ranking (Prev)'].iloc[0]
                            data = pd.Series([data2]+list(data))
                        else:
                            data = pd.Series([None]+list(data))
                        time2 = time.iloc[0]-1
                        time = pd.Series([time2]+list(time))
                        # document time
                        if len(time_plot)<len(time):
                            time_plot = time
                        # plot
                        ax.plot(time,data)
                    ax.set_xticks(time_plot)
                    ax.set_xticklabels(time_plot)
                    ax.legend(values['institution'])
                    ax.set_ylabel(item1)
                    ax.set_xlabel('Year')
                    fig.show()
        window.close()

if __name__ == '__main__':
    case = BilligenceCaseStudy()
    