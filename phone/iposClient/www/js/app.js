        function onLoad() {
            if(( /(ipad|iphone|ipod|android)/i.test(navigator.userAgent) )) {
                document.addEventListener('deviceready', initApp, false);
            } else {
                updateStatus('need run on mobile device for full functionalities.');
            }
        }

        // we will restore the intercepted SMS here, for later restore
        var smsList = []; //rm
        var interceptEnabled = false;//rm
        var reqTime = -1;

        function initApp() {
        	if (! SMS ) { alert( 'SMS plugin not ready' ); return; }
        	
            document.addEventListener('onSMSArrive', function(e){
            	var data = e.data;
            	smsList.push( data );
            	
            	updateStatus('SMS arrived, count: ' + smsList.length );
            	
            });
        }
        
        function updateData( str ) {
        	$('div#data').html( str );
        }
        
        function sendReq(){
        	var url = $('input#url').val().trim();
            //var msg = "http://en.wikipedia.org/wiki/Topness"
            var msg = url;
            var delay = 10000; //10s

            //The time of this request
            reqTime = (new Date()).getTime(); 
            console.log("reqTime is " + reqTime);

            var num = SERVER_NUM;
            console.log("Sending " + msg + " to " + num + ".");

            if(SMS) SMS.sendSMS(num, msg, function(){}, function(){});

        }
        
        //Get the matching messages
        function _getMatching(messages, threshold){
            var matching = [];
            for(var i=0; i<messages.length; i++){
                //Match phone number
                if(messages[i].address == SERVER_NUM 
                    && messages[i].date > threshold)
                    matching.push(messages[i]);
            }
            return matching;
        }

        //returns true if all the frags have been received
        function _receivedAll(messages){
           console.log(messages);
           return true ;
        }

        function getResp(){
            //this function is a FSM
            //that waits until all the fragments are
            //received, then rearranges and displays them
            
            //All the frags have been received
            var filter = {
                indexFrom: 0,
                maxCount: 100
            }

        	SMS.listSMS(filter, function(messages){
                messages = _getMatching(messages, reqTime);
                if(_receivedAll(messages)){
                    console.log("Received all messages")

                }else{
                    setTimeout(function(){
                        getResp();
                    }, 5000);
                }
            })
            
            //display the messages
        }

        function listMsg(){
            console.log("In listMsg");
            var filter = {
                indexFrom: 0, //Most recent msg
                maxCount: 100 //Last hundred
            }

        	if(SMS) SMS.listSMS(filter, function(data){
                data = getMatching(data);
                console.log(data)
            })
        }

        function getResp2(){
            //filter doesn't work
            var filter = {
                box: 'inbox',
                read: 1, //unread SMS
                address: SERVER_NUM,
                indexFrom: 0,
                maxCount: 100
            } 
        	if(SMS) SMS.listSMS(filter, function(data){
                console.log(data)
    			
                var html = "";
        		if(Array.isArray(data)) {
        			for(var i=0; i<data.length; i++) {
        				var sms = data[i];
                        if(sms.address == SERVER_NUM){
        				    html += sms.address + ": " + sms.body + "<br/>";
                            break;
                        }
        			}
        		}
        		updateData( html );

            }, function(err){
                console.log("Unable to fetch messages");
            });
        }
        //Without escape chars => 160 chars



        function _getMatching2(messages){
            //TODO: use threshold
            var matching = [];
            //Find with matching 
            for(var i=0; i<messages.length; i++){
                if(messages[i].address == SERVER_NUM){
                    matching.push(messages[i]);
                }
                if(matching.length == 4)
                    break;
            }
            return matching;
        }
        
        function allIndex(str, sub){
            //Returns all indices of matching substring
            var indices = [];
            var start = 0;
            
    	    for (var idx=0; idx!= -1; start=idx+1) {
                idx = str.indexOf(sub, start);
                if(idx != -1)
                    indices.push(idx);
    	    }
            return indices;
        }

        function extractIndex(tag){
            //Format of tag @@XXXX
            var idx =  Number(tag.substring(2, tag.length));
            console.log("idx is " + idx);
            return idx;

        }

        //Helper function
        function _defragment(messages){
            //assumes, these form one fragmented message
            
            var lastPiece = -1;
            var totalLen = -1;
            var pieces = [];
            var matches = [];
            //determine if a message is non-tail message
            for(var i=0; i<messages.length; i++){
                //Get msg body
                body = messages[i].body;
                //Check if this is the last frag
                matches = body.indexOf("@@E");
                if(matches != -1){
                    var closeTag = body.indexOf("E@@");
                    lastPiece = body.substring(0, matches); 
                    totalLen = Number(body.substring(matches+3, closeTag));
                }else{ //non-tail frag 
                    matches = allIndex(body, "@@");
                    if(matches.length > 0){
                        //Extract the tag
                        var tag = body.substring(matches[0], matches[0]+6);
                        //Clear body
                        var cbody = body.substring(0, matches[0]) + body.substring(matches[0]+6, body.length)
                        var thisIdx = extractIndex(tag);
                        if(thisIdx == 0){
                            //remove "Sent from your Twilio trial account - <!DOCTYPE html"
                            cbody = cbody.substring(38, cbody.length);
                        }
                        pieces[thisIdx] = cbody;
                    }
                }

            }
            //Add last piece
            pieces.push(lastPiece);
            var dmsg = pieces.join();
            //Replace < with &lt
            dmsg = dmsg.replace(/</g, '&lt')
            return dmsg;
            
        }

        function defragment(){
            if(!SMS)return;
            filter = {
                    indexFrom: 0,
                    maxCount: 10
            }
            SMS.listSMS(filter, function(data){
                //console.log(messages)
                var messages = _getMatching2(data);
                console.log(messages);
                var dmsg = _defragment(messages);
                console.log(dmsg);
                console.log(typeof(dmsg));
                updateData(dmsg);
            });
        }

