# Task: Replace the item TIMESTAMP_UTC in every row with a new item NewValue.
# Input: A parsed data list with TIMESTAMP_UTC.
# Output: The same list with the item replaced.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example iterates through all rows and replaces the "TIMESTAMP_UTC" item
# with a new one

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
    end_idx = CreateVarParam(-1)
    is_row_end_sign = CreateVarParam(False)
    while datain.FindRow(start_idx, end_idx, is_row_end_sign):
        end_idx1 = end_idx.value
        end_idx2 = end_idx1
        if is_row_end_sign.value:
            end_idx2 -= 1

        for idx in range(start_idx, end_idx2):
            item = datain.Items[idx]
            if (item.Name == 'TIMESTAMP_UTC'):
                item = None # remove reference to the item, because we'll delete it (free allocated memory)
                datain.Delete(idx)
                datain.InsertItem(idx, 'NewValue', int(123))
        row_cnt += 1
        if row_cnt > 5: break

        start_idx = end_idx1 + 1

def ParseData(callparams, datasource, buffer, dataout):
    # do nothing
    pass

def ExportData(callparams, datasource, datain):
    # do nothing
    pass

main()