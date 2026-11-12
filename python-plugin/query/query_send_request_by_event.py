# Task: Send one request to the device right after its port is opened (event PORT-OPEN).
# Input: The PORT-OPEN event.
# Output: The bytes hello, world sent to the data source.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example sends a request only once, after data source opening

from plugin import *

plugin_name = 'Test plugin'
send_count = 0

def main():
    global plugin_name

    print('Loaded: ' + plugin_name)

def FilterData(callparams, datasource, datain, dataout):
    # do nothing
    pass

# event_params - list with all event parameters (depends on the event)
# datasource - data source ID (can be None)
# event - event name

def EventData(event_params, datasource, event):
    global send_count

    print('Event: ' + str(event))

    if event == 'PORT-OPEN':
        print("Sending request")
        send_count += 1

        data = bytes(b'hello, world')
        SendData(datasource, data)

def ParseData(callparams, datasource, buffer, dataout):
    # do nothing
    pass

def ExportData(callparams, datasource, datain):
    # do nothing
    pass

main()