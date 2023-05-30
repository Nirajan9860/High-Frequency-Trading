import requests


class MarketDataProvider:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.marketdataprovider.com'

    def get_market_data(self, symbol):
        endpoint = f'/market/{symbol}/data'
        headers = {'Authorization': f'Bearer {self.api_key}'}

        try:
            response = requests.get(self.base_url + endpoint, headers=headers)
            response.raise_for_status()  # Raise an exception if the request was not successful
            market_data = response.json()
            return market_data
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving market data for symbol {symbol}: {e}")
            return None
