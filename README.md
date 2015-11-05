IPOS -> IP over SMS 

A client/server architecture to send/receive IP traffic 
over SMS.

Problem
=======
Many service providers provide "Unlimited" text messages.
Having access to data (mobile broadband) typically is a separate
feature.

In fact many places only have access to GSM (2G).

The ability to provide IP over SMS would provide IP to users
that otherwise don't have it, or where the cost is very high.

For the purposes of document, we will refer to SMS as 
specified in RFC 5724:
https://www.ietf.org/rfc/rfc5724.txt


Overview
========

1) First we need a IP to SMS encoder.

2) Second, we need a broker, i.e. a 
computer with access to the network.

3) The client phone, should either have: 1) a special 
browser that explicity sends SMS, or 2) a custom
firmware that can intercept outgoing packets.
In the first case, the browser could just wrap HTTP requests
in SMS. In the second case, we would need to intercept
all IP datagrams originating from the browser and wrap 
those in SMS.


Broker, should strip images, advertisments, and other
unncessary content

Architecture
============
1) User makes an HTTP request through the browser. 

2) The browser wraps the HTTP traffic in SMS and 
sends it to the broker.

3)The broker makes the request.

4)The broker receives the response.

5)The broker parses the response and and removes 
any non-text, and unncessary elements.

6)The broker passes the response to the requester.

7)The user agent displays the results.

Challenges
==========
Bandwidth available over SMS

Extensions
===========
Use that peer to peer distributed storing service, 
and create a NDN for content. 

Encode images as strings -> will eat a lot of bandwidth.

References
==========
HTTP
    http://www.w3.org/Protocols/rfc2616/rfc2616.txt
