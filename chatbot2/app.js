'use strict';

// Imports dependencies and set up http server
const
    express = require('express'),
    bodyParser = require('body-parser'),
    app = express().use(bodyParser.json()); // creates express http server

// var handlePostback = require('./app');

const PAGE_ACCESS_TOKEN = "EAAbSXaZCiipYBAPgmdZAvHEMYsC4IPm61KJNMuINWvaZCUJ8MVQV3QShyaooGLRWgmK2Rsi7tBnZBndr27vW21D8SoZC5fQHdFllXFd7QNDHt1SQIwYsiTZB4CKmT64BTU24wnjkgHlKfOlTRs6zpils0svdX2QNymaBDn12xZAWMobnNb9niTh"

const request = require('request');

var arr = [];

// Sets server port and logs message on success
app.listen(27019, () => console.log('webhook is listening on port 27019'));

// Creates the endpoint for our webhook
app.post('/webhook', (req, res) => {

    let body = req.body;

    // Checks this is an event from a page subscription
    if (body.object === 'page') {

        // Iterates over each entry - there may be multiple if batched
        body.entry.forEach(function (entry) {

            // Gets the body of the webhook even
            if (entry.messaging[0]) {
                let webhook_event = entry.messaging[0];

                // Get the sender PSID
                let sender_psid = webhook_event.sender.id;
                console.log('Sender PSID: ' + sender_psid);

                // Check if the event is a message or postback and
                // pass the event to the appropriate handler function
                if (webhook_event.message) {
                    handleMessage(sender_psid, webhook_event.message);
                }
            }
        });


        // Returns a '200 OK' response to all requests
        res.status(200).send('EVENT_RECEIVED');
    } else {
        // Returns a '404 Not Found' if event is not from a page subscription
        res.sendStatus(404);
    }

});

// Adds support for GET requests to our webhook
//this function only reads verifytoken for somereason
app.get('/webhook', (req, res) => {

    // Your verify token. Should be a random string.
    let VERIFY_TOKEN = "EAAbSXaZCiipYBAC9SrwumZChslClTbttIw2yCguHZARSP1JHTeZA5rbawsO0oJXrAHGD39aYSeeQU7boOZBigH3ENkDBBd4XZBZBwBtcR2PahsrrLZAt2pMa6pOZCbZCPu9pN44tlvW3Hzz3rZAZA9GRYuxiZCSRr3TZBrADP1jI5kKbUflgnxqKUITZCtq"

    // Parse the query params
    let token = req.query['hub.verify_token'];
    let mode = req.query['hub.mode'];
    let challenge = req.query['hub.challenge'];

    console.log(req.body);
    // Checks if a token and mode is in the query string of the request
    if (mode && token) {
        console.log('got the params at least');
        // Checks the mode and token sent is correct
        if (mode === 'subscribe' && token === VERIFY_TOKEN) {

            // Responds with the challenge token from the request
            console.log('WEBHOOK_VERIFIED');
            res.status(200).send(challenge);

        } else {
            // Responds with '403 Forbidden' if verify tokens do not match
            res.sendStatus(403);
        }
    }
});

app.get('/sendTexts', (req, res) => {
    console.log('hi');
    //sending to everyone subscibed a text rn
    console.log(arr);
    for (var i = arr.length - 1; i >= 0; i--) {
        console.log(arr[i]);
        callSendAPI(arr[i], {"text": "right about now is a good time to invest"})
    }
    res.sendStatus(200);
});


function handleMessage(sender_psid, received_message) {
    let response;
    // Check if the message contains text
    console.log(received_message);
    if (received_message.text) {
        if (received_message.text === "subscribe") {
            arr = arr.concat(sender_psid);
            response = {"text": "Happy Mining"};
        } else if (received_message.text === "unsubscribe") {
            response = {"text": "No longer Mining? I hope you have a wonderful day with government controlled currency"};
            for (var i = arr.length - 1; i >= 0; i--) {
                if (arr[i] === sender_psid) {
                    arr.splice(i, 1);
                }
            }
        } else if (received_message.text === "invest") {
            request({
                "uri": "http://35.190.144.249:27019/invest"
            }, (err, res, body) => {
                if (!err) {
                    console.log('message sent!');
                    let r = JSON.parse(body);

                    if (r["invest"] === "yes") {
                        response = {"text": "You should invest!"}
                    } else {
                        response = {"text": "Nah man!"}
                    }
                    callSendAPI(sender_psid, response);
                } else {
                    console.error("Unable to send message:" + err);
                }
            });
        } else {
            // Create the payload for a basic text message
            response = {"text": "HI!!!"};
        }
    }
    console.log(response);
    // Sends the response message
    callSendAPI(sender_psid, response);
}

// Sends response messages via the Send API
function callSendAPI(sender_psid, response) {
    // Construct the message body
    let request_body = {
        "recipient": {
            "id": sender_psid
        },
        "message": response
    };
    console.log(request_body);
    // Send the HTTP request to the Messenger Platform

    request({
        "uri": "https://graph.facebook.com/v2.6/me/messages",
        "qs": {"access_token": PAGE_ACCESS_TOKEN},
        "method": "POST",
        "json": request_body
    }, (err, res, body) => {
        if (!err) {
            console.log('message sent!');
            console.log(response);
        } else {
            console.error("Unable to send message:" + err);
        }
    });
}