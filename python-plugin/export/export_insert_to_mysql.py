# Task: Insert the time stamp and the data packet of every row into a MySQL table with mysql.connector.
# Input: A parsed data list with DATE_TIME_STAMP and DATA_PACKET.
# Output: Rows in the table data_log.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example shows how to insert parsed data to a database (e.g. MySQL)

from plugin import *
import mysql.connector
import datetime
import time

plugin_name = 'Test plugin'
insert_count = 0
mydb = None

def main():
    global plugin_name, mydb

    print('Loaded: ' + plugin_name)

    # connects to a database on plugin loading
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="test",
            passwd="123",
            database="test"
        )
    except mysql.connector.Error as error:
        print('Unable to connect: ' + str(error))

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
    global insert_count, mydb
    if(mydb == None):
        print('Not connected')
        return

    myquery = "INSERT INTO data_log(DATESTAMP,SCANNER_ID,BARCODE) VALUES(%s,%s,%s)"

    mycursor = mydb.cursor()
    try:
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

            # the parser have to prepare and add these items
            # for example, you may use our ASCII Data Parser or the corresponding Python example
            timestamp = datain.ItemValueByName('DATE_TIME_STAMP', start_idx, end_idx2)
            value = datain.ItemValueByName('DATA_PACKET', start_idx, end_idx2)

            # prepares a time stamp string from tupple
            timestamp_s = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
            print('Timestamp: ' + timestamp_s)
            print('Value: ' + str(value))

            if timestamp is not None:
                try:
                    args = (timestamp_s, 1, value)
                    mycursor.execute(myquery, args)
                except mysql.connector.Error as error:
                    print('Unable to insert data: ' + str(error))

            start_idx = end_idx.value + 1                   

    except mysql.connector.Error as error:
        print('Unable to allocate cursor: ' + str(error))
    finally:
        mycursor.close()

main()
