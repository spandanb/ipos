"""
Send messages using Twilio
"""

from twilio.rest import TwilioRestClient 
from flask import Flask, request, redirect
import os

#Requires TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN env variables
client = TwilioRestClient()

def send(to=os.environ["PHONE_NUMBER_TO"], body="Hello there" ):
    #Sends a message to 'to' with message 'body'

    print 'Sending "{}" to {}'.format(body, to)
    
    #Send the message
    client.messages.create( 
        to=to,
        from_=os.environ["PHONE_NUMBER_FROM"], 
        body=body,  
    )

if __name__ == "__main__":
    send()
