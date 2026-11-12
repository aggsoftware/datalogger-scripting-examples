# Task: Call the plugin API functions one after another: GetModuleParameter, DbgLog, SendEvent, SendEventEx, SendByte, SendString, SendDataToDataSource and DiscardDataPacket.
# Input: None.
# Output: Log messages, events and bytes to COM3.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example calls the plugin API functions one by one
import plugin
from plugin import *

plugin_name = 'Test plugin'
send_timer = None

def main():
    global plugin_name

    print('Loaded2: ' + plugin_name)

    value = GetModuleParameter("ModulePath")
    print('Module path: ' + str(value))

    DbgLog("Error message", 0)
    DbgLog("Warning message", 1)
    DbgLog("Info message", 2)

    SendEvent("MY-TEST-EVENT")

    event_args = ['VALUE_NAME1', 1, 'VALLUE_NAME2', 123.0, 'OTHER_VALLUE_NAME', 'string data', 'BOOL_VALUE_NAME', True]
    SendEventEx("MY-TEST-EVENT-WITH-ARGS", event_args)    

    SendByte(None, 123)
    SendString(None, "#00text string with encoded hex values#0D#0A")

    data = bytes(b'hello, world')
    datasource = 'COM3' # a text name of the destination data source as you see it in the main window
    SendDataToDataSource(datasource, data)

def FilterData(callparams, datasource, datain, dataout):
    # this function works in filters only and filter out all data in a single data packet   
    DiscardDataPacket()    

main()
