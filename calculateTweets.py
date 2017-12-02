from pymongo import MongoClient
from sentiment import analyzeSentiment
from datetime import datetime, timedelta

client = MongoClient(host="35.227.77.242", port=27019)
db = client['mad_invest']

collection = db["tweets"]

def runUpdateScoreMangitude():
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

def returnScoreMagnitudeByHour(timestamp):
    time = (timestamp - timedelta(hours=1)).timestamp()*1000
    cursor = collection.find({'timestamp_ms': {"$gt": str(time),"$lt": str(timestamp.timestamp()*1000)}})
    score = []
    magnitude = []
    for document in cursor:
        something = document['score']
        print(something)
        score.append(document["score"])
        magnitude.append(document["magnitude"])
    return {score,magnitude}



if __name__ == '__main__':
    print(returnScoreMagnitudeByHour(datetime.now()-timedelta(hours=1)))
    #runUpdateScoreMangitude()
