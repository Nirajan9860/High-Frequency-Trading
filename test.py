import datetime
import time
import tkinter as tk

import matplotlib.pyplot as plt
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


class MovingAverageCrossover:
    def __init__(self, fast_period, slow_period):
        self.fast_period = fast_period
        self.slow_period = slow_period

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


class Portfolio:
    def __init__(self, starting_capital):
        self.starting_capital = starting_capital
        self.capital = starting_capital
        self.positions = []
        self.portfolio_value_history = []
        self.timestamp_history = []

    def add_position(self, symbol, quantity, average_price):
        position = {
            'symbol': symbol,
            'quantity': quantity,
            'average_price': average_price
        }
        self.positions.append(position)

    def calculate_portfolio_value(self, market_data):
        portfolio_value = self.capital

        for position in self.positions:
            symbol = position['symbol']
            quantity = position['quantity']
            average_price = position['average_price']

            # Look up the current market price for the symbol in market_data
            current_price = next(
                item['price'] for item in market_data if item['symbol'] == symbol)

            # Calculate the position value and add it to the portfolio value
            position_value = current_price * quantity
            portfolio_value += position_value

        return portfolio_value

    def update_portfolio_history(self, portfolio_value, timestamp):
        self.portfolio_value_history.append(portfolio_value)
        self.timestamp_history.append(timestamp)


class RiskManager:
    def __init__(self, max_loss_percent):
        self.max_loss_percent = max_loss_percent

    def check_stop_loss(self, portfolio, market_data):
        portfolio_value = portfolio.calculate_portfolio_value(market_data)
        loss_percent = (portfolio_value - portfolio.starting_capital) / \
            portfolio.starting_capital * 100

        if loss_percent <= -self.max_loss_percent:
            return True  # Stop loss triggered
        else:
            return False


class TradingSystem:
    def __init__(self, starting_capital, fast_period, slow_period, max_loss_percent):
        self.market_data_provider = MarketDataProvider()
        self.trading_algorithm = MovingAverageCrossover(
            fast_period, slow_period)
        self.portfolio = Portfolio(starting_capital)
        self.risk_manager = RiskManager(max_loss_percent)

        self.root = tk.Tk()
        self.root.title("Trading System Dashboard")

        self.fig = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.start_button = tk.Button(
            self.root, text="Start Trading", command=self.start_trading)
        self.start_button.pack(side=tk.BOTTOM)

    def start_trading(self):
        self.start_button.config(state=tk.DISABLED)
        self.run_trading_system()

    def run_trading_system(self):
        while True:
            current_data = self.market_data_provider.get_market_data(
                self.portfolio.symbols)
            previous_data = current_data[:-1]  # Use all but the latest data

            position_size = self.trading_algorithm.calculate_position_size(
                current_data, previous_data)
            # Example: Use the first symbol in the current data
            symbol = current_data[0]['symbol']

            if position_size == 1:
                self.execute_buy_trade(symbol)
            elif position_size == -1:
                self.execute_sell_trade(symbol)

            if self.risk_manager.check_stop_loss(self.portfolio, current_data):
                self.execute_stop_loss()
                break

            self.monitor_portfolio()

            self.root.update()
            time.sleep(1)  # Sleep for 1 second before the next iteration

    def execute_buy_trade(self, symbol):
        # Trading account required
        pass

    def execute_sell_trade(self, symbol):
        # Trading account required
        pass

    def execute_stop_loss(self):
        # Tradin account required
        pass

    def monitor_portfolio(self):
        market_data = self.market_data_provider.get_market_data(
            self.portfolio.symbols)
        portfolio_value = self.portfolio.calculate_portfolio_value(market_data)
        timestamp = datetime.datetime.now()
        self.portfolio.update_portfolio_history(portfolio_value, timestamp)

        self.plot_portfolio_history()

    def plot_portfolio_history(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(self.portfolio.timestamp_history,
                self.portfolio.portfolio_value_history)
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Portfolio Value')
        ax.set_title('Portfolio Value Over Time')
        ax.tick_params(axis='x', rotation=45)

        self.canvas.draw()

    @property
    def symbols(self):
        # Retrieve the symbols from the portfolio positions
        return [position['symbol'] for position in self.portfolio.positions]


# Example usage
starting_capital = 10000
fast_period = 10
slow_period = 30
max_loss_percent = 10

trading_system = TradingSystem(
    starting_capital, fast_period, slow_period, max_loss_percent)

trading_system.root.mainloop()
