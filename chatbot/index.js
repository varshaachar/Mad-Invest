'use strict'

const bodyParser = require('body-parser'),
      express = require('express'),
      request = require('request'),
      app = express()

app.set('port', (process.env.PORT || 5000))

// Allows us to process the data
app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())

// ROUTES 
app.get('/', function(req, res){
    res.send("Hi I am a chatbot!")
})

// Facebook
// kinda like passwords, security

app.get('/webhook/', function(req, res){
    if (req.quey['hub.verify_token'] === "let's hope this works"){
        res.send(req.query['hub.challenge'])
    }
    res.send("Wrong token")
})

// Get request
app.post('/webhook/', function(req, res0{
    let messaging_events = req.body.entry[0].messaging_events
    for (let i = 0; i < messaging_events.length; i++){
        let event = messaging_events[i]
            let sender  event.sender.id
            if (event.message && event.message.text){
                let text = event.message.txt
                sendText(sender, "Text echo: " + text.substring(0, 1000))
            }
    }
    res.sendStatus(200)
})


// Starts server, by listening to requests. URL, you send requests. Server listens to requests @ port #, so it can send a response. 
app.listen(app.get('port'), function(){
    console.log("running: port")
})

// Procfile - is for whoever we're hosting this chatbot. We are using node for web application, with entry point app.js

