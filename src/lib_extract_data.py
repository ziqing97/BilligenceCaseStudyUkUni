"""
Created on Sun Jan 28 13:47:32 2024

@author: yuziq
"""
import copy
import numpy as np
import pandas as pd

def read_data_from_file(file:str) -> pd.DataFrame:
    """read the given excel file

    Args:
        file (str): path to the file

    Returns:
        pd.DataFrame: Dataframe which stores the data
    """
    df_file = pd.read_excel(file)
    return df_file

def filter_range(df:pd.DataFrame,field:str,vmin:float,vmax:float) -> pd.Series:
    """filter the dataframe using a specific factor in given range

    Args:
        df (pd.DataFrame): origin dataframe
        field (str): the factor to be filtered
        vmin (float): min value
        vmax (float): max value

    Returns:
        pd.Series: a series of condition in true or false
    """
    condition = ((df.loc[:,field]>=vmin) & (df.loc[:,field]<=vmax)) | (df.loc[:,field].isnull())
    return condition

def filter_choose(df:pd.DataFrame,field:str,chosen_list:list) -> pd.Series:
    """filter the dataframe which includes the elements in a specific column

    Args:
        df (pd.DataFrame): origin dataframe
        field (str): the factor to be filtered
        chosen_list (list): the chosen elements

    Returns:
        pd.Series: a series of condition in true or false
    """
    chosen_list_copy = copy.deepcopy(chosen_list)
    condition = df[field].isin(chosen_list_copy)
    return condition

def category_in_institution(df:pd.DataFrame)->dict:
    """to category the origin data into different instituions

    Args:
        df (pd.DataFrame): origin dataframe

    Returns:
        dict: a python dict with key as the institutions and the
        values as the dataframe for this institution
    """
    df_dict_in_institution = {}
    institutions =   df['Institution'].unique()
    for item in institutions:
        df_temp = df[df['Institution'] == item]
        df_temp = df_temp.sort_values(by='Ranking Year',ascending=True)
        df_dict_in_institution[item] = df_temp.reindex()
    return df_dict_in_institution

def category_in_year(df:pd.DataFrame)->dict:
    """to category the origin data into different years

    Args:
        df (pd.DataFrame): origin dataframe

    Returns:
        dict: a python dict with key as the year and the
        values as the dataframe in this year
    """
    df_dict_in_year = {}
    years =   df['Ranking Year'].unique()
    for item in years:
        df_temp = df[df['Ranking Year'] == item]
        df_dict_in_year[item] = df_temp.reindex()
    return df_dict_in_year

def update_df(df:pd.DataFrame)->tuple:
    """to category the dataframe in year, institution and
    extract all fields

    Args:
        df (pd.DataFrame): origin dataframe

    Returns:
        tuple: the categoriezed dataframe and all fields
    """
    df_dict_in_year = category_in_year(df)
    df_dict_in_institution = category_in_institution(df)
    fields = list(df.columns.values)
    return fields,df_dict_in_year,df_dict_in_institution

def row_type_for_table(df:pd.DataFrame,fields:list)->dict:
    """
    determine if a column is number of text, if number, find the range
    if text, find the deduplicated list
    Args:
        df (pd.DataFrame): a dataframe
        fields (list): one or more table headings in the dataframe

    Returns:
        dict: a dict stores the information of the given fields
    """
    type_dict = {}
    df = df.reset_index()
    for item in fields:
        if isinstance(df.loc[0,item],np.int64) or isinstance(df.loc[0,item],float):
            type_dict[item] = {'type':'range'}
            value_min = df.loc[:,item].min()
            value_max = df.loc[:,item].max()
            type_dict[item]['min'] = value_min
            type_dict[item]['max'] = value_max
        else:
            type_dict[item] = {'type':'multiselect'}
            type_dict[item]['values'] = df[item].unique()
    return type_dict
