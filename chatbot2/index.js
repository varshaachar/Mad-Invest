'use strict';

// Imports dependencies and set up http server
const
  express = require('express'),
  bodyParser = require('body-parser'),
  app = express().use(bodyParser.json()); // creates express http server

// var handlePostback = require('./app');
var handleMessage = require('./app');

// Sets server port and logs message on success
//app.listen(process.env.PORT || 1337, () => console.log('webhook is listening'));
app.listen(27019, () => console.log("listening on port 3000"));


// Creates the endpoint for our webhook
app.post('/webhook', (req, res) => {

  let body = req.body;

  // Checks this is an event from a page subscription
  if (body.object === 'page') {

    // Iterates over each entry - there may be multiple if batched
    body.entry.forEach(function(entry) {

      // Gets the body of the webhook even
        if(entry.messaging[0]) {
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
