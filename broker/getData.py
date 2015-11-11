# -*- coding: UTF-8 -*-

"""
This module gets text from request url.
This is achieved in 2 parts: 1) getting the page,
2) cleaning the page
"""
import requests
#from libextract.api import extract
import re
import sys
from streamData import emulateSms 
from utils import is_esc_char, byte_len, chunk_iter_offset, prologue
"""
There are two parts to this: 1)get the page, 
and parse the data.

To get the page, use requests. 

To manually parse the page, use beautifulSoup.

Alternatively, use a Content Extraction library 
to get boilerplate content.

"""

#NOTE: For now let's ignore auth issues, 
#i.e. accessing only publicly available pages

#NOTE: May need to use a headless browser
#especially if JS is creating/changing content

#TODO: parse should be able to parse to varying  
#levels based on bandwidth requirments

def rmNonAscii(string):
    return ''.join([c for c in string if ord(c)<128])


def getResp(url):
    """
    Returns the response corresponding 
    to GET on url
    """
    resp = requests.get(url)
    return resp

#def parse(page, rm_newline=True, rm_non_ascii=True):
#    """
#        Arguments:
#        page- the page as a string
#        rm_newline- remove \n
#    """
#    #Extract: str-> generator (5 elements)
#    #type(textnodes) -> lxml.etree._ElementUnicodeResult
#    textnodes = list(extract(page))
#    text = textnodes[0].text_content()
#
#    if rm_newline:
#        text = re.sub('\n', '', text)
#    
#    if rm_non_ascii:
#        text = rmNonAscii(text) 
#
#    return text
#
#def getText(url):
#    """
#    Get the content on the page specified by
#    the url
#    """
#    page = getResp(url)
#    text = parse(page.content)
#    return text

def tag_message2(msg):
    """
    This tags the message with identifiers
    such that they can be ordered
    """
    MSG_LEN = 160
    #Tag Format is @@XXXX -> can order upto 9999 messages
    # = 9999 bytes
    TAG_LEN = 6
    #The step size while iterating over msg
    STEP = MSG_LEN - TAG_LEN

    #Get tag
    # index -> @@XXXX
    get_tag = lambda i: "@@" + str(i).zfill(4) 
    
    #Get tagged chunk
    get_tagged = lambda i, chunk: get_tag(i) + chunk

    #"Sent from your Twilio trial account - ".length == 38
    OFFSET = 38
    chunks = []
    #Append the first chunk
#    chunks.append(get_tag(0) + msg[0: STEP - OFFSET])
    #Iterate over msg len at step interval
#    for i,j in enumerate(range(STEP - OFFSET, len(msg), STEP)):
#        #i iterates over number of chunks
#        #j iterates over index in message
#        chunks.append(get_tag(i+1) + msg[j:j+STEP])
   
    
    indices = []
    start_index = -1
    i = 0
    for char in msg:
        if i%STEP == 0:
            #start index
            start_index = i

        elif (i+1) % STEP == 0:
            #end index
            indices.append((start_index, i))

        #increment index
        if is_esc_char(char):
            i+=2
        else:
            i+=1

        #if first_chunk:
    print indices
    #msg = ''.join(chunks)
    #Add an end tag
    #msg += "@@@@@@"
    #return msg

def tag_message(msg):
    MSG_LEN = 160
    #Tag Format is @@XXXX -> can order upto 9999 messages
    # = 9999 bytes
    TAG_LEN = 6
    #The step size while iterating over msg
    STEP = MSG_LEN - TAG_LEN

    #Get tag
    # index -> @@XXXX
    get_tag = lambda i: "@@" + str(i).zfill(4) 
    
    #Get tagged chunk
    get_tagged = lambda i, chunk: get_tag(i) + chunk
    
    offset = STEP - len(prologue)
    
    chunks = []
    for i, chunk in enumerate(chunk_iter_offset(msg, size=STEP, offset=offset)):
        chunks.append(get_tagged(i, chunk))

    return "".join(chunks)

def getPage(url, max_len=400, tag_msg=True):
    """
    Get the page
    """
    #NOTE: To get the images/css/js files, need to parse
    # response to see the linked file and make requests for those
    
    r = requests.get(url, stream=True)
    page = [chunk for chunk in r.iter_content() ]
    page = "".join(page)
    page = rmNonAscii(page)
    page = page[0: max_len]
    if tag_msg:
        page = tag_message(page)
    return page


def test1():
    url ="http://en.wikipedia.org/wiki/Topness"
    page = getPage(url)
    for chunk in emulateSms(page, size=160):
        print chunk
        print byte_len(chunk)
        print "-------------------------------"


if __name__ == "__main__":
    test1()

