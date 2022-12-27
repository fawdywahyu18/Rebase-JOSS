"""
Run rebase_os.py

@author: fawdywahyu
"""

from rebase_os import *

# import data
data_cpi = pd.read_excel('CPI.xlsx')
data_ts = data_cpi.set_index('Date')

rebased_data = main_run(data_ts, y_index=1, x_index=0, method_input='wa')
rebased_data.to_excel('CPI-Rebased.xlsx')
