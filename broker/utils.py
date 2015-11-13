# -*- coding: UTF-8 -*-
"""
Utility functions
"""

import re
import pdb

#Need to account for escape chars 
#since escape characters take 2 bytes
#Matches | [ ] { } ~ \ €
esc_char = re.compile(ur"[|\[\]{}~\\€]")

is_esc_char = lambda c: not not esc_char.match(c)

prologue = "Sent from your Twilio trial account - "

def byte_len(string):
    """
    Gives the length of the string
    with respect to number of 
    bytes consumed in transmission
    """
    length = 0
    for char in string:
        if is_esc_char(char):
            length += 2
        else:
            length += 1
    return length

def chunk_iter(data, size=160): 
    """
    Iterates over `data` and yields
    constant byte `size` substrings
    """
    
    can_peak = lambda i, data: i < len(data)-1 
    
    #iterates over bytes
    #emit packet when byte_idx = size-1
    #or byte_idx = size -2, if next char is 
    #an esc char
    start_idx = -1
    byte_idx = 0
    for i, char in enumerate(data):
        #print "i={}, b={}, char={}".format(i,byte_idx, char)
        #Keep track of chunk start
        if byte_idx  == 0:
            start_idx = i

        #Increment byte_idx
        if is_esc_char(char):
            byte_idx += 2
        else:
            byte_idx += 1

        #Check if chunk can be emitted
        if byte_idx == size:
            #At capacity-> emit chunk 
            yield data[start_idx: i+1]
            byte_idx = 0

        #Peak
        elif byte_idx == size-1:
            #we have capacity to send one char
            #if next char will require 
            #2 bytes, emit the current chunk 
            if can_peak(i,data) and is_esc_char(data[i+1]):
                yield data[start_idx: i+1]
                byte_idx = 0

    #yield any remaining chars
    if byte_len(data) % size != 0:
        yield data[start_idx:]

def chunk_iter_offset(data, size=160, offset=0):
    """
    Iterates over `data` and yields
    constant byte `size` substrings
    `offset` is the size of the first chunk
    """
    #Handle offset
    if offset > size:
        print "ERROR: offset must be less than size"
        return

    if offset > 0:
        for chunk in chunk_iter(data, size=offset):
            yield chunk 
            break
        tail = data[offset:]
    
    for chunk in chunk_iter(tail, size=size):
        yield chunk

def test1():
    data1 = "0123456789" #Base case
    data2 = "012[456789" #i-case #why is this special
    data3 = "0123[456789" #i+1case
    for chunk in chunk_iter(data3, size=5):
        print "BYTE_LEN= {} CHUNK= {}".format(byte_len(chunk), chunk)
    

if __name__ == "__main__":
    test1()
