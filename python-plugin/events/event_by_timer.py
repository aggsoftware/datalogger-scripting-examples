# Task: Raise a custom event MY-EVENT with a Unix time stamp every 5 seconds from a timer thread.
# Input: None.
# Output: MY-EVENT with VALUE for the Events notification plugin or other scripts.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example generates an event by a timer
import time
import datetime
import threading
import atexit
import signal
import plugin
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

def generate_event():
    global send_timer
   
    ms = datetime.datetime.now()
    unix_timestamp = int(time.mktime(ms.timetuple()))
    print('Timestamp: ', unix_timestamp)

    event_args = ['VALUE', unix_timestamp]
    SendEventEx("MY-EVENT", event_args)

def main():
    global plugin_name, send_timer

    print('Loaded: ' + plugin_name)

    # the timer calls a function every N seconds
    send_timer = RepeatableTimer(5.0, generate_event) # executes some actions every N seconds
    send_timer.start()
    print('main() exit')

def exit_handler():
    global send_timer;
    print('My application is ending!')
    if send_timer is not None:
        send_timer.cancel();
        send_timer = None

atexit.register(exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGINT, exit_handler)

main()