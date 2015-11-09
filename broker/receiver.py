"""
This module is the server and responsible for
and responding to received message
"""
#Tutorial here:
#   https://www.twilio.com/docs/quickstart/python/sms/hello-monkey 
from flask import Flask, request, redirect
import twilio.twiml
import os
from getData import getPage

app = Flask(__name__)
 
def get_url(message):
    """
    Extract the URL from 
    the request sent by the client
    """
    url = message.strip()
    return url


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    #Twilio Requests:
    #https://www.twilio.com/docs/api/twiml/sms/twilio_request

    print "Receieved message {} from {}".format(
                request.form['Body'], request.form['From'])
    
    #The request
    req = request.form['Body']
    #The request url 
    url = get_url(req)
    print "Requested URL is {}".format(url)
    
    #Note Twilio limits the sms size to 1600 chars
    #It will do the fragmentation 
    #However there is no ordering guarantee 
    page = getPage(url)

    #Response
    resp = twilio.twiml.Response()
    resp.message(page)
    return str(resp)
 
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
