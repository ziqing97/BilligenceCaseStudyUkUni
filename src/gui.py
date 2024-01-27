# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 18:39:37 2024

@author: yuziq
"""

import PySimpleGUI as sg
layout = [  [sg.Text('Load the data')],
            [sg.Text('Give the data here'), sg.input(),sg.FileBrowse()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

window = sg.Window('UK Uni Case Study', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()