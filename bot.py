import threading
import time

from market_data_provider import MarketDataProvider
from order_executor import OrderExecutor
from trading_algorithm import MovingAverageCrossover

# Define constants and configurations
SYMBOL = 'AAPL'
MARKET_DATA_INTERVAL = 5  # in seconds
MAX_POSITION_SIZE = 1000
STOP_LOSS_PERCENTAGE = 5

# Instantiate market data provider, trading algorithm, and order executor
market_data_provider = MarketDataProvider()
trading_algorithm = MovingAverageCrossover()
order_executor = OrderExecutor()

# Define a function for retrieving market data and triggering trading decisions


def process_market_data():
    while True:
        # Retrieve real-time market data
        market_data = market_data_provider.get_market_data(SYMBOL)

        # Apply trading algorithm to make trading decisions
        position_size = trading_algorithm.calculate_position_size(market_data)
        if position_size > MAX_POSITION_SIZE:
            position_size = MAX_POSITION_SIZE

        # Execute trades
        if position_size > 0:
            order_executor.execute_market_order(SYMBOL, position_size)
        elif position_size < 0:
            stop_loss_price = market_data['price'] * \
                (1 - STOP_LOSS_PERCENTAGE / 100)
            order_executor.execute_stop_order(
                SYMBOL, position_size, stop_loss_price)

        # Wait for the specified interval before processing the next market data
        time.sleep(MARKET_DATA_INTERVAL)


# Start a separate thread to retrieve market data and trigger trades
market_data_thread = threading.Thread(target=process_market_data)
market_data_thread.start()

# Main program loop
while True:
    # Perform other tasks or continue with additional functionality
    # ...

    # Pause or exit the program when desired
    if user_input == 'pause':
        market_data_thread.pause()
    elif user_input == 'exit':
        market_data_thread.stop()
        break
