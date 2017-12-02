from pymongo import MongoClient
from sentiment import analyzeSentiment

client = MongoClient(host="35.227.77.242", port=27019)
db = client['mad_invest']

collection = db["tweets"]

cursor = collection.find({'lang': 'en'})
for document in cursor:
    text = document["text"]
    arr = analyzeSentiment(text)
    score = arr[0]
    magnitude = arr[1]
    id = document["_id"]
    collection.update_one({'_id' : id}, {
        '$set':
            {"score": score, "magnitude": magnitude}
    })