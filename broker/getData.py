"""
This module gets text from request url.
This is achieved in 2 parts: 1) getting the page,
2) cleaning the page
"""
import requests
#from libextract.api import extract
import re
import sys
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

def getPage(url):
    """
    Get the page
    """
    #NOTE: To get the images/css/js files, need to parse
    # response to see the linked file and make requests for those
    
    r = requests.get(url, stream=True)
    page = [chunk for chunk in r.iter_content() ]
    page = "".join(page)
    page = rmNonAscii(page)
    return page

if __name__ == "__main__":
    url ="http://en.wikipedia.org/wiki/Information_extraction"
    url ="http://en.wikipedia.org/wiki/Topness"
    page = getPage(url)
    print page

