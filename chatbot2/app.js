const PAGE_ACCESS_TOKEN="EAAbSXaZCiipYBAPgmdZAvHEMYsC4IPm61KJNMuINWvaZCUJ8MVQV3QShyaooGLRWgmK2Rsi7tBnZBndr27vW21D8SoZC5fQHdFllXFd7QNDHt1SQIwYsiTZB4CKmT64BTU24wnjkgHlKfOlTRs6zpils0svdX2QNymaBDn12xZAWMobnNb9niTh"

module.exports = handleMessage;
module.exports = handlePostback;

// Handles messages events
function handleMessage(sender_psid, received_message) {
      let response;

      // Check if the message contains text
      if (received_message.text) {
        if(received_message.test)
        // Create the payload for a basic text message
        response = {"text": `You sent the message: "${received_message.text}". Now send me an image!`
        }
      }

  // Sends the response message
  callSendAPI(sender_psid, response);
}

// Handles messaging_postbacks events
function handlePostback(sender_psid, received_postback) {
    let response;

    // Get the payload for the postback
    let payload = received_postback.payload;

    // Set the response based on the postback payload
    if (payload === 'yes') {
      response = { "text": "Thanks!" }
    } else if (payload === 'no') {
      response = { "text": "Oops, try sending another image." }
    }
    // Send the message to acknowledge the postback
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
  }
  console.log(request_body);
  // Send the HTTP request to the Messenger Platform
    var request = require('request');
    request({
    "uri": "https://graph.facebook.com/v2.6/me/messages",
    "qs": { "access_token": PAGE_ACCESS_TOKEN },
    "method": "POST",
    "json": request_body
  }, (err, res, body) => {
    if (!err) {
      console.log('message sent!')
    } else {
      console.error("Unable to send message:" + err);
    }
  });
}