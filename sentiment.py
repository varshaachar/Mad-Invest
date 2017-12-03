import requests

API_KEY = "AIzaSyCxt3mIzVk9pLxnk8I0i29S2FLSVPhaacg"

url = "https://language.googleapis.com/v1/documents:analyzeSentiment?key=" + API_KEY

# The text to analyze
def analyzeSentiment(text):
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
    read = r.json()
    #[score,magnitude]
    return [read["documentSentiment"]["score"], read["documentSentiment"]["magnitude"]]
    # return read


if __name__ == '__main__':
    from mad_invest.config import db

    for tweet in db["tweets"].find({"lang": "en"}).limit(100):
        sen = analyzeSentiment(tweet["text"])
        sen["_id"] = tweet["_id"]
        db["sentiments"].insert_one(sen)
        print(sen)
