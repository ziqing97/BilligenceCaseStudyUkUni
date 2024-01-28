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
    
def category_in_institution(df):
    df_dict_in_institution = {}
    institutions =   df['Institution'].unique()
    for item in institutions:
        df_temp = df[df['Institution'] == item]
        df_temp = df_temp.sort_values(by='Ranking Year',ascending=True)
        df_dict_in_institution[item] = df_temp.reindex()
    return df_dict_in_institution

def category_in_year(df):
    df_dict_in_year = {}
    years =   df['Ranking Year'].unique()
    for item in years:
        df_temp = df[df['Ranking Year'] == item]
        df_dict_in_year[item] = df_temp.reindex()
    return df_dict_in_year

def update_df(df):
    df_dict_in_year = category_in_year(df)
    df_dict_in_institution = category_in_institution(df)
    fields = list(df.columns.values)
    return fields,df_dict_in_year,df_dict_in_institution