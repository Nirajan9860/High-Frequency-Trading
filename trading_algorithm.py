from backtester import Backtester
from market_data_provider import MarketDataProvider

market_data_provider = MarketDataProvider()

SYMBOL = 'AAPL'


class MovingAverageCrossover:
    def __init__(self, fast_period, slow_period, market_data):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.market_data = market_data

    def calculate_position_size(self, current_data, previous_data):
        fast_ma = self.calculate_moving_average(current_data, self.fast_period)
        slow_ma = self.calculate_moving_average(current_data, self.slow_period)

        if fast_ma > slow_ma:
            return 1  # Buy signal
        elif fast_ma < slow_ma:
            return -1  # Sell signal
        else:
            return 0  # No signal

    def calculate_moving_average(self, data, period):
        prices = [item['price'] for item in data[-period:]]
        return sum(prices) / period


algorithm = MovingAverageCrossover(fast_period=10, slow_period=30)
# current_data = [...]  # Current market data in the form of a list of dictionaries
# previous_data = [...]  # Previous market data in the form of a list of dictionaries
market_data = market_data_provider.get_market_data(SYMBOL)
for i in range(1, len(market_data)):
    current_data = market_data[i]
    previous_data = market_data[i - 1]


position_size = algorithm.calculate_position_size(current_data, previous_data)
print(f"Position size: {position_size}")
