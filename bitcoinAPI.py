# import PyMongo and connect to a local, running Mongo instance
from pymongo import MongoClient
import gdax
import requests

class PublicClient(object):
    """GDAX public client API.
    All requests default to the `product_id` specified at object
    creation if not otherwise specified.
    Attributes:
        url (Optional[str]): API URL. Defaults to GDAX API.
    """

    def __init__(self, api_url='https://api.gdax.com'):
        """Create GDAX API public client.
        Args:
            api_url (Optional[str]): API URL. Defaults to GDAX API.
        """
        self.url = api_url.rstrip('/')
        
    def _get(self, path, params=None):
        """Perform get request"""

        r = requests.get(self.url + path, params=params, timeout=30)
        # r.raise_for_status()
        return r.json()
    
    def get_product_historic_rates(self, product_id, start=None, end=None,granularity=None):
        params = {}
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        if granularity is not None:
            params['granularity'] = granularity

        return self._get('/products/{}/candles'.format(str(product_id)), params=params)
    
    
def main():
    client = MongoClient(host="35.227.77.242", port=27019)
    db = client["mad_invest"]
    bit_data =  PublicClient()
    print bit_data.get_product_historic_rates('BTC-USD', '2010-12-01','2017-12-07')
    
if __name__ == "__main__":
    main()