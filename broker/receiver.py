"""
This module is the server and responsible for
and responding to received message
"""
#Tutorial here:
#   https://www.twilio.com/docs/quickstart/python/sms/hello-monkey 
from flask import Flask, request, redirect
import twilio.twiml
import os

app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    #Twilio Requests:
    #https://www.twilio.com/docs/api/twiml/sms/twilio_request

    print "Receieved message {} from {}".format(
                reques.form['Body'], request.form['From'])

    #Response
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)
 
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
