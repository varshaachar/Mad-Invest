import logging

import time

import requests
from docopt import docopt
import mad_invest.data_sources.twitter as twitter
from mad_invest.oracle import average_sentiment
from mad_invest.sentiment import get_sentimental as sentiment

l = logging.getLogger(__name__)

HELP = """
Mad-Invest

Usage:
  run.py twitter
  run.py sentiment
  run.py sarah
  
twitter: run twitter daemon
sentiment: run sentiment analysis daemon
  
"""


def sarah():

    inv = average_sentiment(lookback=600)

    if inv > 0:
        l.debug("Good time %s", inv)

        r = requests.get("https://mic-conf.com/sendTexts")

        return r.text

    time.sleep(60)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s [ %(threadName)s ] [ %(levelname)s ] : %(message)s'")

    arguments = docopt(HELP, version='Mad-Invest 0.1')
    l.debug(arguments)

    if arguments["twitter"]:
        twitter.main()
    if arguments["sentiment"]:
        sentiment()
    if arguments["sarah"]:
        while True:
            sarah()
