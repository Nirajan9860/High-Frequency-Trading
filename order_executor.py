import requests


class OrderExecutor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.orderexecutor.com'

    def execute_market_order(self, symbol, quantity):
        endpoint = '/orders'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {
            'symbol': symbol,
            'quantity': quantity,
            'type': 'market',
            'side': 'buy' if quantity > 0 else 'sell'
        }

        try:
            response = requests.post(
                self.base_url + endpoint, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception if the request was not successful
            order_id = response.json().get('order_id')
            print(f"Market order executed successfully. Order ID: {order_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error executing market order: {e}")

    def execute_stop_order(self, symbol, quantity, stop_price):
        endpoint = '/orders'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {
            'symbol': symbol,
            'quantity': quantity,
            'type': 'stop',
            'side': 'buy' if quantity > 0 else 'sell',
            'stop_price': stop_price
        }

        try:
            response = requests.post(
                self.base_url + endpoint, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception if the request was not successful
            order_id = response.json().get('order_id')
            print(f"Stop order executed successfully. Order ID: {order_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error executing stop order: {e}")


order_executor = OrderExecutor(api_key='YOUR_API_KEY')
symbol = 'AAPL'
quantity = 100
stop_price = 150.0

order_executor.execute_market_order(symbol, quantity)
order_executor.execute_stop_order(symbol, quantity, stop_price)
