"""
Tools for dealing with pickles

"""

import logging
import pickle

l = logging.getLogger(__name__)


def load_pickle(path):
    """
    Load a pickle object from path

    :param str path:
    :return: the pickle object loaded
    :rtype: object
    """

    with open(path, "rb") as f:
        l.debug("Opening pickle at %s", path)
        r = pickle.loads(f.read())
    return r


def write_pickle(path, data):
    """
    Write date to a pickle path

    :param str path:
    :param object data:
    :return: path of the written pickle
    :rtype: str
    """

    with open(path, "wb") as f:
        l.debug("Writing pickle at %s", path)
        f.write(pickle.dumps(data))
    return path
