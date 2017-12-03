import logging

from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from keras.models import load_model

from mad_invest.config import db
from mad_invest.deli import load_pickle
from mad_invest.trainner import get_labels, prepare_texts, tokenise
from mad_invest.oracle import average_sentiment

app = Flask(__name__)
l = logging.getLogger(__name__)

tknz = load_pickle("tknz.pickle")
model = load_model("three_model.h5")


def predict(text):
    global tknz
    global model

    data, word_index, tknz = tokenise(text, tokenizer=tknz)
    return model.predict(data).mean()


@app.route("/predict")
def predict_on():
    text = request.args.get("text")

    return jsonify({"predict": float(predict(text))})


@app.route('/invest')
def invest():
    avg_sen = average_sentiment(lookback=600)
    if avg_sen <= 0:
        return jsonify({"avg_sen": avg_sen, "invest": "no"})
    else:
        return jsonify({"avg_sen": avg_sen, "invest": "yes"})


@app.route('/tweets')
def get_tweets():
    l.debug("Args: %s", request.args)

    ts = int(request.args.get("ts") or datetime.now().timestamp() * 1000)

    tweets = db["tweets"].find({"lang": "en",
                                'timestamp_ms': {"$gte": ts},
                                "score": {"$exists": True}})

    return jsonify(list(tweets))
