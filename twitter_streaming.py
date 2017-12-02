# YHack 2017 - Getting bitcoin tweets from Twitter

# Inputs: keyword to be searched
# Output: prints a dictionary with tweets and its details (for entered keyword(s))

import tweepy
#from tweepy.streaming import StreamListener, json
from tweepy import Stream

# The consumer keys and access tokens which are used to authenticate the connection

consumer_key = '3bXfYDio2BdN2KsisVTKteHIo'
consumer_secret = '8QnZCAIBAxoDu3q0tGGStUeR4FkqxRmvdRVj3nMGjrEjILrZJ6'
access_token = '935969840606732288-gpAG1w7lEwsdJeedb5pFZ7mu3KQbi9E'
access_token_secret = 'oIE83ro4AkIBpom1nP5G3WTl8BFyF0XJFMCIHSzJr4Ziw'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        pass

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = MyStreamListener()
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keyword 'bitcoin'
    data = stream.filter(track=['bitcoin'])
    print(data)