"""
Open Source Software for Rebase data (Splice data)

@author: fawdywahyu
"""

import pandas as pd
import numpy as np
from datetime import timedelta

def detect_overlapp(x=None, y=None):
    # X: slice of dataframe, X adalah data yang akan diubah tahun dasarnya
    # Y: slide of dataframe, Y adalah data yang tahun dasarnya digunakan
    
    # x = data_ts.iloc[:,0]
    # y = data_ts.iloc[:,1]
    
    list_not_nax = x[x.notna()].index.tolist()
    list_not_nay = y[y.notna()].index.tolist()
    list_overlap = list(set(list_not_nax) & set(list_not_nay))
    list_overlap.sort()
    
    if len(list_overlap)==0:
        result_check = 'There is no overlapp observations'
    else:
        result_check = list_overlap
    
    return result_check


def splice_data(x=None, y=None, method=None, growth_overlapp=None):
    # X: slice of dataframe, X adalah data yang akan diubah tahun dasarnya
    # Y: slide of dataframe, Y adalah data yang tahun dasarnya digunakan
    # method: string yang memiliki opsi
        # 1. Cumulative Weighted Average = cumwa
        # 2, Weighted Average = wa
    # growth_overlapp : list yang berisi float string (tanggal) dan float (lag value of y)
    # yang akan digunakan apabila tidak ada data overlapp.
    # growth_overlapp merupakan data tingkat pertumbuhan saat terjadi data overlapp.
    # index dalam list digunakan untuk tau tanggal berapa kedua data diasumsikan overlap
    
    # x = data_ts.iloc[:,0]
    # y = data_ts.iloc[:,1]
    # method = 'cumwa'
    # growth_overlapp = [0.04, '2018-01-01']
    
    idx_overlapp = detect_overlapp(x, y)
    
    if idx_overlapp=='There is no overlapp observations':
        idx_growth_timestamp = pd.Timestamp(growth_overlapp[1])
        last_month = idx_growth_timestamp - timedelta(days=30)
        last_month_idx = pd.Timestamp(f'{last_month.year}-{last_month.month}-{idx_growth_timestamp.day}')
        last_value = y[last_month_idx]
        growth_overlapp.append(last_value)
        
        if len(growth_overlapp)!=3:
            raise Exception('You run the growth method but there is no lag value of y')
        
        y_overlapp = growth_overlapp[-1] + (growth_overlapp[-1] * growth_overlapp[0])
        x_overlapp = x[idx_growth_timestamp]
        adj_factor = y_overlapp/x_overlapp
    else:
        x_overlapp = x[idx_overlapp[0]:idx_overlapp[-1]]
        y_overlapp = y[idx_overlapp[0]:idx_overlapp[-1]]
        
        if method=='cumwa':
            adj_factor = np.sum(y_overlapp)/np.sum(x_overlapp)
        elif method=='wa':
            adj_factor = np.mean([y_overlapp[i]/x_overlapp[i] for i in range(len(y_overlapp))])
        else:
            raise Exception('Method is unrecognized')
    
    x_adj = x * adj_factor
    
    return x_adj


# Modify in this part
def main_run(data_input=None, date_index=None, freq_input=None,
             y_index=None, x_index=None, method_input=None,
             growth_overlapp_input = None):
    # data_input : dataframe with date column
    # date_index : int which contains index to date column
    # freq_input : the frequency of timeseries data, example 'MS'
    # y_index: int yang berisi index data y
    # x_index: int yang berisi index data x
    # method_input: str antara 'wa' atau 'cumwa'
    # growth_overlapp : list yang berisi int (0-1) float string (tanggal)
    # yang akan digunakan apabila tidak ada data overlapp.
    # int berguna untuk memberikan info tingkat pertumbuhan month on month saat data overlapp
    
    # data_input = data_cpi
    # date_index = 0
    # freq_input = 'MS'
    # y_index = 0
    # x_index = 1
    # method_input = 'wa'
    
    ts_index = pd.date_range(start=data_input.iloc[:,date_index][0],
                             periods=len(data_input.iloc[:,date_index]),
                             freq=freq_input)
    columns_df = data_input.columns
    data_ts = data_input.set_index(ts_index).drop(columns_df[date_index],
                                                  axis=1)
    
    y_slice = data_ts.iloc[:,y_index]
    x_slice = data_ts.iloc[:,x_index]
    
    rebase_x = splice_data(x=x_slice, y=y_slice, method=method_input,
                           growth_overlapp=growth_overlapp_input)
    
    # substitute y in data_ts
    data_ts.iloc[:,x_index] = rebase_x
    data_ts.rename(columns={columns_df[(x_index+1)]:'New Base Year'}, inplace=True)
    
    return data_ts

# import data
data_cpi = pd.read_excel('CPI.xlsx')

rebased_data = main_run(data_cpi, date_index=0, freq_input='MS', 
                        y_index=0, x_index=1, method_input='cumwa',
                        growth_overlapp_input=[0.02, '2018-01-01'])
rebased_data.to_excel('CPI-Rebased.xlsx')
