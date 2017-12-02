import logging

from docopt import docopt
import mad_invest.data_sources.twitter as twitter
from mad_invest.sentiment import get_sentimental as sentiment

l = logging.getLogger(__name__)

HELP = """
Mad-Invest

Usage:
  run.py twitter
  run.py sentiment
  
twitter: run twitter daemon
sentiment: run sentiment analysis daemon
  
"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s [ %(threadName)s ] [ %(levelname)s ] : %(message)s'")

    arguments = docopt(HELP, version='Mad-Invest 0.1')
    l.debug(arguments)

    if arguments["twitter"]:
        twitter.main()
    if arguments["sentiment"]:
        sentiment()
