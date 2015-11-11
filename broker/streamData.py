"""
This module is responsible for 
"""
from utils import is_esc_char, byte_len, chunk_iter, chunk_iter_offset
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


def emulateSms(data, size=160, add_prologue=True):
    """
    Emulates how some arbitrary text string will be 
    fragmented when sent over SMS using Twilio
    """
    
    #Twilio enforces this restriction
    if byte_len(data) > 1600:
        print "Unable to end message longer than 1600 chars"
        return

    if add_prologue: 
        prologue = "Sent from your Twilio trial account - "
        data = prologue + data

    for chunk in chunk_iter(data, size=size):
        yield chunk

def test1():
    data = "012345678[9"
    for sms in emulateSms(data, size=5, add_prologue=False):
        print '"{}", byte_len is {}'.format(sms, byte_len(sms))
        print "------------------"

def test2():
    data = "012345678[9"
    for sms in chunk_iter_offset(data, size=5, offset=3):
        print '"{}", byte_len is {}'.format(sms, byte_len(sms))
        print "------------------"


if __name__ == "__main__":
    test2()
