# Task: Walk through the rows of an incoming data list and print their index ranges. The skeleton for any row-based filter.
# Input: A parsed data list.
# Output: Unchanged data; row information in the log.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example iterates through all rows

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
    start_idx = 0
    end_idx = CreateVarParam(-1)
    is_row_end_sign = CreateVarParam(False)
    row_cnt = 0
    while datain.FindRow(start_idx, end_idx, is_row_end_sign):
        end_idx2 = end_idx.value
        print('Row: ' + str(row_cnt))
        print('Start index: ' + str(start_idx))
        print('End index: ' + str(end_idx2))
        if is_row_end_sign.value:
            end_idx2 -= 1
        row_cnt += 1
        if row_cnt > 5: break
        start_idx = end_idx.value + 1

def ParseData(callparams, datasource, buffer, dataout):
    # do nothing
    pass

def ExportData(callparams, datasource, datain):
    # do nothing
    pass

main()