import math
import copy
import pandas as pd

def read_data_from_file(file):
    # extract the extend filename
    df_file = pd.read_excel(file)
    return df_file

def filter_range(df,field,vmin,vmax):
    value_min = math.ceil(df.loc[:,field].min())
    value_max = int(df.loc[:,field].max())
    if vmin<value_min or vmax>value_max:
        raise ValueError('invalid range')
    else:
        condition = (df.loc[:,field]>vmin) & (df.loc[:,field]<vmax)
        return condition

def filter_choose(df,field,chosen_list):
    chosen_list_copy = copy.deepcopy(chosen_list)
    condition = df[field].isin(chosen_list_copy)
    return condition
    
