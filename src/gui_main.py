# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 13:47:32 2024

@author: yuziq
"""

import PySimpleGUI as sg
import lib_extract_data as led
sg.theme("DarkBlue3")
sg.set_options(font=("Microsoft JhengHei", 16))
class BilligenceCaseStudy():
    def __init__(self):
        self.dataframe = None
        self.fields = []
        self.main()

    def main(self):
        layout_load = [  [sg.Text('Functions')],
                    [sg.Button('Load data'), sg.Button('Compare data in same year'),\
                     sg.Button('Compare trend'), sg.Button('Prediction')],\
                    [sg.Button('Cancel')]]
        
        window = sg.Window('UK Uni Case Study', layout_load)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            else:
                if event == 'Load data':
                    self.gui_read_data()
                # load new window according to the event
        window.close()

    def gui_read_data(self):
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
                pass
                # self.dataframe = led.combine_df(self.dataframe,dataframe.temp)      
            self.fields,self.df_dict_in_year,self.df_dict_in_institution = \
                led.update_df(self.dataframe)    
            print(self.dataframe)
        window.close()
    
    def gui_table_view(self):
        layout_table = [  [sg.Text('Load the data')],
                    [sg.Text('Give the data here'),sg.Input(),sg.FileBrowse()],
                    [sg.Button('Ok'), sg.Button('Cancel')] ]
        
        window = sg.Window('UK Uni Case Study', layout_table)

    def gui_trend_view(self):
        pass
    
    def gui_prediction_view(self):
        pass

if __name__ == '__main__':
    case = BilligenceCaseStudy()
    