# -*- coding: UTF-8 -*-
"""
Utility functions
"""

import re


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
        if byte_idx  == 0:
            start_idx = i

        elif byte_idx == size-1:
            yield data[start_idx: i+1]
            byte_idx = 0
            continue

        #Peak
        elif byte_idx == size-2:
            #we only have capacity to send one
            #more byte but next char will require 
            #2 bytes
            if can_peak(i,data) and is_esc_char(data[i+1]):
                yield data[start_idx: i+1]
                byte_idx = 0
                continue

        #Increment byte_idx
        if is_esc_char(char):
            byte_idx += 2
        else:
            byte_idx += 1

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
        print "ERROR: offset must be greater than size"
        return

    if offset > 0:
        for chunk in chunk_iter(data, size=offset):
            yield chunk 
            break
        data = data[offset:]
        
    for chunk in chunk_iter(data, size=size):
        yield chunk
