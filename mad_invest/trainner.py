"""
Train a model for BitCoin price prediction using Keras
"""
import logging
from datetime import datetime
import pandas as pd
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
import os

MAX_NB_WORDS = None
MAX_SEQUENCE_LENGTH = 100000
EMBEDDING_DIM = 100

l = logging.getLogger(__name__)


def tokenise(texts):
    """
    Tokenise the text and convert it to nicely formatted matrices

    :param texts:
    :return:
    """
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)

    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

    return data, word_index


def string_process(x):
    x = x.values
    return " ".join([str(xs) for xs in x])


def prepare_texts(paths, labels):
    df = pd.DataFrame()
    for p in paths:
        l.info("Concatting %s", p)
        ndf = pd.read_csv(p)
        df = pd.concat(df, ndf)
    return prepare_text(df)


def prepare_text(df, labels):
    """
    Load the csv of comments and prepare the text to be fed into the model

    :param path:
    :return:
    """

    df["dt"] = pd.to_datetime(df["created_utc"], unit="s").dt.round("1h")

    data = pd.DataFrame(df.groupby("dt")["body"].apply(string_process))

    r = pd.concat([labels, data], axis=1).dropna(how="any", axis=0)

    return r["body"], r["target"]


def get_labels(start_month=8):
    df3 = pd.read_csv("./data/hourlybtc.csv")

    df3["dt"] = pd.to_datetime(df3["ts"], unit="s")

    monthly = df3[
        (df3["dt"] >= datetime(2017, start_month, 1, 0, 0, 0)) & (df3["dt"] <= datetime(2017, 11, 1, 0, 0, 0))]

    reg = pd.DataFrame()

    reg["dt"] = monthly["dt"].dt.round("1h")
    reg["p"] = monthly["price"]

    reg["dp"] = reg["p"].diff()

    reg["dp"] = reg["dp"].shift(-1)

    reg["target"] = reg["dp"].map(lambda x: 0 if x <= 0 else 1)

    reg = reg.set_index("dt")
    return reg


def prepare_label(labels):
    labels = to_categorical(np.asarray(labels))
    print('Shape of label tensor:', labels.shape)

    return labels


def train(data, labels, word_index):
    # split the data into a training set and a validation set
    indices = np.arange(data.shape[0])
    np.random.shuffle(indices)
    data = data[indices]
    labels = labels[indices]
    nb_validation_samples = int(0.3 * data.shape[0])

    x_train = data[:-nb_validation_samples]
    y_train = labels[:-nb_validation_samples]
    x_val = data[-nb_validation_samples:]
    y_val = labels[-nb_validation_samples:]

    embeddings_index = {}
    f = open(os.path.join("data", 'glove.twitter.27B.100d.txt'))
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()

    print('Found %s word vectors.' % len(embeddings_index))

    embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector

    embedding_layer = Embedding(len(word_index) + 1,
                                EMBEDDING_DIM,
                                weights=[embedding_matrix],
                                input_length=MAX_SEQUENCE_LENGTH,
                                trainable=False)

    # train a 1D convnet with global maxpooling
    sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
    embedded_sequences = embedding_layer(sequence_input)
    x = Conv1D(128, 5, activation='relu')(embedded_sequences)
    x = MaxPooling1D(5)(x)
    x = Conv1D(128, 5, activation='relu')(x)
    x = MaxPooling1D(5)(x)
    x = Conv1D(128, 5, activation='relu')(x)
    x = GlobalMaxPooling1D()(x)
    x = Dense(128, activation='relu')(x)
    preds = Dense(2, activation='softmax')(x)

    model = Model(sequence_input, preds)
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['acc'])

    model.fit(x_train, y_train,
              batch_size=128,
              epochs=10,
              validation_data=(x_val, y_val))

    return model


def main():
    labels = get_labels(start_month=8)
    texts, labels = prepare_texts(
        ['./data/comments_17_08.csv', './data/comments_17_09.csv', './data/comments_17_10.csv'], labels=labels)
    data, word_index = tokenise(texts)
    labels = prepare_label(labels)
    m = train(data, labels, word_index)
    m.save("three_model.h5")


if __name__ == '__main__':
    main()
