"""
Handles the broker/server side logic
"""
from getText import getText
from streamData import dataStream
from send import sendToPhone

def broker(url):
    """
    Communicates with the phone 
    """
    text = getText(url)
    for data in dataStream(text, size=100, total=299):
        sendToPhone(body=data)

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Annus_mirabilis"
    broker(url)
