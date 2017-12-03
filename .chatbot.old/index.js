'use strict'

const bodyParser = require('body-parser'),
      express = require('express'),
      request = require('request'),
      app = express()

let token = "EAAbSXaZCiipYBAODjS7GzXzBPB3ZBi699pmF0JxZCwTMyJwozBl4DYsSNuTTYaxi1kCqRLjdZA1af3VuHDdvyDDY4tNRf9Iovgd9ZAT2iALrDdm0Yr8ZCm2NfjvAdTE7BeslJRpU4JVZCUZAaGRwD1SEoOrYJERFVSbnCixAtwJ4bnOOmTFnRnFC"

// ROUTES 
app.get('/', function(req, res){
    res.send("Hi I am a chatbot!")
})

// Facebook
// kinda like passwords, security

app.get('/webhook/', function(req, res){
    if (req.query['hub.verify_token'] === "madinvest"){
        res.send(req.query['hub.challenge'])
    }
    res.send("Wrong token")
})

// sends the text back
app.post('/webhook/', function(req, res){
    let messaging_events = req.body.entry[0].messaging_events
    for (let i = 0; i < messaging_events.length; i++){
        let event = messaging_events[i]
            let sender = event.sender.id
            if (event.message && event.message.text){
                let text = event.message.text
                sendText(sender, "Text echo: " + text.substring(0, 100))
            }
    }
    res.sendStatus(200) // aka ok status
})

// function sendText sends a specific text message
function sendText(sender, text){
    let messageData = {text:text}
    request({
        url:"https://graph.facebook.com/v2.6/me/messages",
        qs : {access_token: token},
        method : "POST",
        json: {
            recipient: {id: sender},
            message : messageData
        }
    }, function(error, response, body){
        if(error){
            console.log("sending error")
        } else if (response.body.error){
            console.log("response body error")
        }
    })
}

// Starts server, by listening to requests. URL, you send requests. Server listens to requests @ port #, so it can send a response. 
app.listen(app.get('port'), function(){
    console.log("running: port")
})

// Procfile - is for whoever we're hosting this chatbot. We are using node for web application, with entry point app.js

