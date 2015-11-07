"""
This module gets text from request url.
This is achieved in 2 parts: 1) getting the page,
2) cleaning the page
"""
import requests
from libextract.api import extract
import re

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

def getPage(url):
    """
    Get page corresponding to url
    """
    resp = requests.get(url)
    return resp

def parse(page, rm_newline=True, rm_non_ascii=True):
    """
        Arguments:
        page- the page as a string
        rm_newline- remove \n
    """
    #Extract: str-> generator (5 elements)
    #type(textnodes) -> lxml.etree._ElementUnicodeResult
    textnodes = list(extract(page))
    text = textnodes[0].text_content()

    if rm_newline:
        text = re.sub('\n', '', text)
    
    if rm_non_ascii:
        text = ''.join(i for i in text if ord(i)<128)

    return text

def getText(url):
    page = getPage(url)
    text = parse(page.content)
    return text

if __name__ == "__main__":
    url ="http://en.wikipedia.org/wiki/Information_extraction"
    print getText(url)

