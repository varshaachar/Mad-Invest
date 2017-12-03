import csv
from pymongo import MongoClient
from sentiment import analyzeSentiment
import logging
from datetime import timedelta

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
            try:
                text = x['text']
                arr = analyzeSentiment(text)
                writer.writerow({'_id': x['_id'], 'score': arr[0], 'magnitude': arr[1], 'date': x['timestamp_ms']})
            except:
                pass

def categorize():
    reader = csv.reader(open('tweets.csv', 'r'), delimiter=',')
    row1 = next(reader)
    row1 = next(reader)
    with open('averages.csv','w') as file:
        fields = ['date', 'score', 'magnitude']
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        compare = (float(row1[3]) / 1000 )+ 3600
        magn=[]
        score=[]
        for row in reader:
            date = (float(row[3]) / 1000 )
            if date <= compare:
                score.append(float(row[1]))
                magn.append(float(row[2]))
            else:
                #add final averages to csv
                writer.writerow({'date': compare, 'score': sum(score) / float(len(score)), 'magnitude':sum(magn) / float(len(magn))})
                magn = []
                score = []
                score.append(float(row[1]))
                magn.append(float(row[2]))
                compare = compare + timedelta(hours=1)
        #once we exit the loop there might still be some data left
        writer.writerow({'date': compare, 'score': sum(score) / float(len(score)), 'magnitude': sum(magn) / float(len(magn))})




if __name__ == '__main__':
    categorize()