# Task: Build a new outgoing data list from the incoming one: one row per source row with its item count.
# Input: A parsed data list.
# Output: A new list with RowCountN items.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This code processes incoming data list, and create a new data list, based on the source data

from plugin import *

plugin_name = 'Test plugin'

def main():
    global plugin_name
    print('Loaded: ' + plugin_name)

# callparams - list with call parameters
# datasource - data source ID (can be None)
# datain - incoming data list
# dataout - outgoing (filtered) data list

def FilterData(callparams, datasource, datain, dataout):
    row_cnt = 0
    start_idx = 0
    end_idx = CreateVarParam(-2)
    is_row_end_sign = CreateVarParam(False)
    while datain.FindRow(start_idx, end_idx, is_row_end_sign):
        end_idx1 = end_idx.value
        end_idx2 = end_idx1
        if is_row_end_sign.value:
            end_idx2 -= 1

        row_size = end_idx2 - start_idx + 1
        dataout.AddItem('RowCount' + str(row_cnt), row_size)
        dataout.NewRow()

        row_cnt += 1

        start_idx = end_idx1 + 1

def ParseData(callparams, datasource, buffer, dataout):
    # do nothing
    pass

def ExportData(callparams, datasource, datain):
    # do nothing
    pass

main()