import datetime
import time

from market_data_provider import MarketDataProvider
from portfolio import Portfolio


class PortfolioMonitor:
    def __init__(self, portfolio, market_data_provider):
        self.portfolio = portfolio
        self.market_data_provider = market_data_provider

    def monitor_portfolio(self):
        # Get current market data
        market_data = self.market_data_provider.get_market_data(
            self.portfolio.symbols)
        current_datetime = datetime.datetime.now()

        # Calculate portfolio value
        portfolio_value = self.portfolio.calculate_portfolio_value(market_data)

        # Print monitoring information
        print(f"Monitoring at {current_datetime}:")
        print(f"Portfolio Value: {portfolio_value}")
        print("Positions:")
        for position in self.portfolio.positions:
            print(
                f"- Symbol: {position['symbol']}, Quantity: {position['quantity']}, Average Price: {position['average_price']}")
        print("-----------------------------------")


portfolio = Portfolio()  # Your portfolio object
market_data_provider = MarketDataProvider()  # Your market data provider object

monitor = PortfolioMonitor(portfolio, market_data_provider)

# Monitor the portfolio at regular intervals or in a loop
while True:
    monitor.monitor_portfolio()
    time.sleep(60)  # Sleep for 1 minute before the next monitoring
