"""
This module is responsible for 
"""

"""
SMS are restricted to 160bytes

The simplest approach is to send the string as is.

To get higher density, we could encode the 
data using a different encodings.

Encodings could be bit-level or character level

This is somewhat useful:
https://www.twilio.com/engineering/2012/11/08/adventures-in-unicode-sms

"""

def dataStream(data, size=160, total=480):
    """
    Generator that returns, size sized strings
    Arguments:
        data: (str), the data to send
        size: the size each substring
        total: total number of characters to send 
    """
    if total<=0:
        ubound = len(data)
    else:
        ubound = min(len(data), total)

    for i in range(0, ubound, size):
        yield data[i:i+size]

