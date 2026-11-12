# Task: Write selected columns of every row to a CSV file, a new file per day.
# Input: A parsed data list with DATE_TIME_STAMP, DATA_PACKET, VALUE1, VALUE2.
# Output: C:\Logs\dataYYYYMMDD.csv, appended.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example creates a CSV file for parsed data.
# The script daily creates a new CSV file

from plugin import *
import datetime
import time

plugin_name = 'Test plugin'

columns = ('DATE_TIME_STAMP', 'DATA_PACKET', 'VALUE1', 'VALUE2')
columns_quote = (1, 1, 0, 0)
csv_separator = ';'
csv_path = 'C:\\Logs\\'


def main():
    global plugin_name

    print('Loaded: ' + plugin_name)


def FilterData(callparams, datasource, datain, dataout):
    # do nothing
    pass


def ParseData(callparams, datasource, buffer, dataout):
    # do nothing
    pass

# callparams - list with call parameters
# datasource - data source ID (can be None)
# datain - incoming data list


def ExportData(callparams, datasource, datain):
    global insert_count
    csv_data = ''

    start_idx = 0
    end_idx = CreateVarParam(-1)
    is_row_end_sign = CreateVarParam(False)
    row_cnt = 0
    while datain.FindRow(start_idx, end_idx, is_row_end_sign):
        end_idx2 = end_idx.value
        if is_row_end_sign.value:
            end_idx2 -= 1

        row_cnt += 1
        print('Row: ' + str(row_cnt))
        row_data = ''

        # the parser have to prepare and add these items
        # for example, you may use our ASCII Data Parser or the corresponding Python example
        for idx in range(len(columns)):
            value = datain.ItemValueByName(columns[idx], start_idx, end_idx2)
            quote_add = columns_quote[idx]
            if value is None:
                value = ''
                quote_add = 0
            elif (type(value) is tuple) and (len(value) == 9):
                # date/time tupple
                value = time.strftime('%Y-%m-%d %H:%M:%S', value)
            else:
                value = str(value)

            if quote_add:
                value = '"' + value + '"'

            row_data = row_data + value + csv_separator

        csv_data = csv_data + row_data + '\n'

        start_idx = end_idx.value + 1

    if len(csv_data) > 0:
        try:
            filename = csv_path + 'data' + datetime.datetime.now().strftime('%Y%m%d') + '.csv'
            with open(filename, 'a') as out:
                try:
                    out.write(csv_data)
                finally:
                    out.close
        except OSError as error:
            print("Unable to write data to a file: {0}".format(error))
        except Exception as error:
            print('Unable to write data to a file: {0}'.format(error))

        start_idx = end_idx.value + 1


main()
