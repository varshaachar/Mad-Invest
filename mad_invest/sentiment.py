import logging

import requests
import time
from mad_invest.config import db

from mad_invest import config

l = logging.getLogger(__name__)
url = "https://language.googleapis.com/v1/documents:analyzeSentiment?key=" + config.GAPI


def analyzeSentiment(text):
    """
    Pass the text through Google Cloud NLP and get the sentiment of the text

    Note: We only take English.

    :param text: The text to analyse
    :return:
    """
    document = {
        'type': 'PLAIN_TEXT',
        'language': 'en',
        'content': text,
    }
    data = {
        'document': document,
        'encodingType': 'utf8'
    }
    r = requests.post(url=url, json=data)
    if r.status_code == 200:
        read = r.json()
        return read
    elif r.status_code == 429:
        time.sleep(1)
        return None


def get_sentimental():
    """
    We will continuously fetch un-analysed data from the database and do sentiment analysis on it.
    """

    while True:
        time.sleep(5)
        to_analyse = db["tweets"].find({"lang": "en", "score": {"$exists": False}}).limit(100)

        for tweet in to_analyse:
            r = analyzeSentiment(tweet["text"])
            if r:
                l.debug("Sentiment for %s is %s", tweet["text"], r)
                score = r["documentSentiment"]["score"]
                magnitude = r["documentSentiment"]["magnitude"]
                db["tweets"].update_one({"_id": tweet["_id"]}, {
                    "$set": {"score": score, "magnitude": magnitude}}, upsert=True)


if __name__ == '__main__':
    for tweet in db["tweets"].find({"lang": "en"}).limit(100):
        sen = analyzeSentiment(tweet["text"])
        sen["_id"] = tweet["_id"]
        db["sentiments"].insert_one(sen)
        print(sen)
