import logging

from mad_invest.api import app

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s [ %(threadName)s ] [ %(levelname)s ] : %(message)s'")

    app.run(host="0.0.0.0", port=27019)
