import json
import logging

import pymongo

import mad_invest.config as config
import tweepy
from tweepy import Stream

from mad_invest.config import db

# The consumer keys and access tokens which are used to authenticate the connection

l = logging.getLogger(__name__)

consumer_key = config.TKEY
consumer_secret = config.TSEC
access_token = config.TAT
access_token_secret = config.TAS

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        d = json.loads(data)
        # l.debug("T: %s", data)
        try:
            l.debug("\n[@%s]: %s", d["user"]["screen_name"], d["text"])
        except Exception as e:
            l.error("Some error", e.args)
            pass
        try:
            d["_id"] = d["id"]
        except:
            l.error("Tweet doesn't have id? %s", data)
        try:
            db["tweets"].insert_one(d)
        except pymongo.errors.DuplicateKeyError as e:
            l.error("Duplicate id: %s", e.args)
            pass
        except Exception as e:
            l.error("Some error", e.args)
            pass

    def on_error(self, status):
        l.error("Stream error: %s", status)

def main():
    # This handles Twitter authentication and the connection to Twitter Streaming API
    listener = MyStreamListener()
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    # This line filter Twitter Streams to capture data by the keyword 'bitcoin'
    to_track = ["bitcoin", "btc", "cypto", "currency", "eth", "etherium", "coin", "mining"]
    l.info("Begin recording stream with keyword: %s", to_track)
    data = stream.filter(track=to_track)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s [ %(threadName)s ] [ %(levelname)s ] : %(message)s'")


