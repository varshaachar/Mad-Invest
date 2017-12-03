import logging

from flask import Flask, request, jsonify
from keras.models import load_model

from mad_invest.trainner import get_labels, prepare_texts, tokenise

app = Flask(__name__)
l = logging.getLogger(__name__)

tknz = None
model = load_model("_octmodel.h5")


def init():
    l.debug("Initial tokeniser")

    labels = get_labels(start_month=8)
    texts, labels = prepare_texts(
        ['./data/comments_17_08.csv', './data/comments_17_09.csv', './data/comments_17_10.csv'], labels=labels)
    data, word_index, tknz = tokenise(texts)


def predict(text):
    global tknz
    global model

    data, word_index, tknz = tokenise(text, tokenizer=tknz)
    return model.predict(data).mean()


@app.route("/predict")
def predict_on():
    text = request.args.get("text")

    return jsonify({"predict": predict(text)})
