import logging
from datetime import datetime, timedelta

from mad_invest.config import db

l = logging.getLogger(__name__)


def average_sentiment(lookback):
    """
    Calculate the average sentiment from now back at lookback, in seconds

    :param lookback: in secs
    :return:
    """

    now = datetime.now()

    uptil = now - timedelta(seconds=lookback)

    docs = db["tweets"].find({
        'timestamp_ms': {"$lte": str(now.timestamp() * 1000),
                         "$gte": str(uptil.timestamp() * 1000)},
        "score": {"$exists": True}
    })
    r = []

    for t in docs:
        l.debug("Examining %s", t)

        score = t["score"]
        mag = t["magnitude"]

        r.append(score * mag * (-1 if score < 0.5 else 1))

    if len(r) == 0: return 0
    return sum(r) / len(r)


if __name__ == '__main__':
    print(average_sentiment(lookback=600))
