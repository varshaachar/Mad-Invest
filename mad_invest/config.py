"""
Config file

DO NOT commit
"""

from pymongo import MongoClient

client = MongoClient(host="35.227.77.242", port=27019)
db = client["mad_invest"]


# Twitter keys

TKEY = '3bXfYDio2BdN2KsisVTKteHIo'
TSEC = '8QnZCAIBAxoDu3q0tGGStUeR4FkqxRmvdRVj3nMGjrEjILrZJ6'
TAT = '935969840606732288-gpAG1w7lEwsdJeedb5pFZ7mu3KQbi9E'
TAS = 'oIE83ro4AkIBpom1nP5G3WTl8BFyF0XJFMCIHSzJr4Ziw'