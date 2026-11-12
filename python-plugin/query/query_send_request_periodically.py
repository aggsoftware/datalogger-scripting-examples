# Task: Send a request to the data source every 5 seconds, five times, from a timer thread, and stop the timer when the plugin unloads.
# Input: None.
# Output: The bytes hello, world sent five times.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example plugin sends a request periodically

import time
import threading
import atexit
import signal
from plugin import *

class RepeatableTimer(threading.Thread):
    def __init__(self, interval, handler):
        threading.Thread.__init__(self)
        self.handler = handler
        self.counter = 0
        self.stopped = threading.Event()
        self.interval = interval

    def run(self):
        while not self.stopped.wait(self.interval):
            self.counter += 1
            self.handler()
            
    def cancel(self):
        self.stopped.set()

plugin_name = 'Test plugin'
send_timer = None
send_count = 0

def hello():
    global send_count, send_timer, plugin
    send_count += 1
    if (send_count <= 5):
        print("Sending request")
        data = bytes(b'hello, world')
        datasource = None # sends data to the default or last data source
        SendData(datasource, data)
    else:
        send_timer.cancel()

def main():
    global plugin_name, send_timer

    print('Loaded: ' + plugin_name)

    send_timer = RepeatableTimer(5.0, hello) # sends "hello, world" 5 times every 5 seconds
    send_timer.start()

    print('Timer started: ' + str(send_timer))

# callparams - list with call parameters
# datasource - data source ID (can be None)
# datain - incoming data list
# dataout - outgoing (filtered) data list

def FilterData(callparams, datasource, datain, dataout):
    # do nothing
    pass

def ParseData(handle, datasource, buffer, dataout):
    # do nothing
    pass

def ExportData(handle, datasource, datain):
    # do nothing
    pass

def exit_handler():
    global send_timer;
    print('My application is ending!')
    # it is necessary to stop the timer thread
    if send_timer is not None:
        send_timer.cancel();
        send_timer = None

atexit.register(exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGINT, exit_handler)

main()