"""
Send messages using Twilio
"""

from twilio.rest import TwilioRestClient 
import os
from getData import getPage

#Requires TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN env variables
client = TwilioRestClient()

def sendToPhone(to=os.environ["PHONE_NUMBER_TO"], body="Hello there" ):
    #Sends a message to 'to' with message 'body'

    print 'Sending "{}" to {}'.format(body, to)
    
    #Send the message
    client.messages.create( 
        to=to,
        from_=os.environ["PHONE_NUMBER_FROM"], 
        body=body,  
    )

if __name__ == "__main__":
    url ="http://en.wikipedia.org/wiki/Topness"
    url ="https://en.wikipedia.org/wiki/Bottom_quark"
    page = getPage(url)
    to_send = page[:400]
    sendToPhone(body=to_send)
