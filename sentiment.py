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
        'encodingType': 'UTF32'
    }
    r = requests.post(url=url, json=data)
    read = r.json()
    #[score,magnitude]
    return [read["documentSentiment"]["score"], read["documentSentiment"]["magnitude"]]

