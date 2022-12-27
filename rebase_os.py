"""
Open Source Software for Rebase data (Splice data)

@author: fawdywahyu
"""

import pandas as pd
import numpy as np

def detect_overlapp(x=None, y=None):
    # X: slice of dataframe, X adalah data dengan tahun dasar yang akan digunakan
    # Y: slide of dataframe, Y adalah data yang akan direbase
    
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
    # X: slice of dataframe, X adalah data dengan tahun dasar yang akan digunakan
    # Y: slide of dataframe, Y adalah data yang akan direbase
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
    # growth_overlapp = [0.04, '2018-01-01', 131.28]
    
    idx_overlapp = detect_overlapp(x, y)
    
    if idx_overlapp=='There is no overlapp observations':
        idx_growth_timestamp = pd.Timestamp(growth_overlapp[1])
        
        if len(growth_overlapp)!=3:
            raise Exception('growth_overlapp argument needs to be a list which has 3 values')
        
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
    
    y_adj = y * adj_factor
    
    return y_adj


# Modify in this part
def main_run(data_ts_input=None, y_index=None, x_index=None, method_input=None):
    # data_ts : dataframe with timeseires index
    # y_index: int yang berisi index data y
    # x_index: int yang berisi index data x
    # method_input: str antara 'wa' atau 'cumwa'
    
    y_slice = data_ts_input.iloc[:,y_index]
    x_slice = data_ts_input.iloc[:,x_index]
    
    rebase_y = splice_data(x=x_slice, y=y_slice, method=method_input)
    
    # substitute y in data_ts
    data_ts_input.iloc[:,y_index] = rebase_y
    
    return data_ts_input








