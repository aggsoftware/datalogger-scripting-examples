# Task: Parse packets of the form <STX>value1;value2;value3<ETX> into FULL_DATA_PACKET, DATA_PACKET, DATA_TIME_STAMP and VALUE1..VALUE3. Shows how a Python parser works with the receive buffer.
# Input: Bytes from the data source, see parser_ascii_data.py.txt.
# Output: A parsed data packet for the filters and export modules.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example parses <STX>value1;value2;value3<ETX> packets

from plugin import *
import datetime

plugin_name = 'Test plugin'

def main():
    global plugin_name

    print('Loaded: ' + plugin_name)

# callparams - list with call parameters
# datasource - data source ID

# datain - incoming data buffer object,
#  The main application allocates a small buffer (65KB) for each data source.
#  Therefore this parser type cannot handle data packets large than the buffer size.
#  The parser should clear the buffer, otherwise it overflows (new data
#  replaces old data)

# dataout - outgoing (parsed) data list.
#  If the parser didn't extract any data, this list should be empty

# this example shows how to parse the simple data packet like:
# <STX>value1;value2;value3<ETX>
# <STX>, <ETX> - ASCII characters with code 0x02 and 0x03
# see: parser_ascii_data.py.txt

# Note: the parser may receive data by small chunks
# Therefore, we should expect that the ending signature will be received later
# (ParseData will be called one more time)

def ParseData(callparams, datasource, buffer, dataout):
    # do nothing
    buff = buffer.GetBytes()
    print('Buffer len1: ' + str(len(buff)))

    idx = buff.find(b'\x02')
    if(idx >= 0):
        if idx > 0:
            buffer.Shift(idx)  # removes N first bytes from the buffer (it does not change 'buff')
            buff = buff[idx + 1:]
        idx = buff.find(b'\x03')
        if idx >= 0:
            full_data_packet = buff[:idx + 1]
            
            # the main application expects to receive the following three variables for
            # each data packet
            # FULL_DATA_PACKET - the data packet with signatures
            # DATA_PACKET - data packet without signatures
            # DATA_TIME_STAMP - parsing local date/time

            # implicit conversion returns data in format b'123455'
            # we need the result as a string

            dataout.AddItem('FULL_DATA_PACKET', full_data_packet.decode('cp1252'))
            data_packet = buff[1:idx].decode('cp1252')
            dataout.AddItem('DATA_PACKET', data_packet)
            dataout.AddItem('DATA_TIME_STAMP', datetime.datetime.now())

            values = data_packet.split(';', 3)
            l = len(values)
            if l > 0:
                dataout.AddItem('VALUE1', values[0])
            if l > 1:
                dataout.AddItem('VALUE2', values[1])
            if l > 2:
                dataout.AddItem('VALUE3', values[2])

            buffer.Clear()  # we do not expect more data in our buffer


main()
