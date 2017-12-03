import pandas
import csv
from pymongo import MongoClient
from sentiment import analyzeSentiment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("averaging")

client = MongoClient(host="35.227.77.242", port=27019)
db = client['mad_invest']

collection = db["tweets"]


def csvCreate():
    cursor = collection.find ({},{'_id':1, 'text': 1, 'timestamp_ms':1})
    i = 0
    logging.info('doing this tweet id' + str(i))
    with open('tweets.csv', 'w') as outfile:
        fields = ['_id','score','magnitude','date']
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for x in cursor:
            i += 1
            logging.info('doing this tweet id: ' + str(i))
            text = x['text']
            try:
                arr = analyzeSentiment(text)
                writer.writerow({'_id': x['_id'], 'score': arr[0], 'magnitude': arr[1], 'date': x['timestamp_ms']})
            except:
                pass

if __name__ == '__main__':
    csvCreate()