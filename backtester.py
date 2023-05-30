from market_data_provider import MarketDataProvider
from riskmanager import RiskManager
from trading_algorithm import MovingAverageCrossover

market_data_provider = MarketDataProvider()
SYMBOL = "AAPL"


class Backtester:
    def __init__(self, market_data, trading_algorithm, risk_manager, starting_capital):
        self.market_data = market_data
        self.trading_algorithm = trading_algorithm
        self.risk_manager = risk_manager
        self.capital = starting_capital
        self.positions = []

    def run_backtest(self):
        for i in range(1, len(self.market_data)):
            current_data = self.market_data[i]
            previous_data = self.market_data[i - 1]

            # Apply trading algorithm to make trading decisions
            position_size = self.trading_algorithm.calculate_position_size(
                current_data, previous_data)

            # Apply risk management rules
            position_size = self.risk_manager.apply_stop_loss(
                current_data, position_size)

            # Execute trades
            if position_size > 0:
                self.execute_trade(current_data, position_size, 'buy')
            elif position_size < 0:
                self.execute_trade(current_data, abs(position_size), 'sell')

    def execute_trade(self, market_data, quantity, side):
        # Simulate trade execution based on market data and quantity
        trade_price = market_data['price']
        trade_value = trade_price * quantity
        trade_cost = trade_value * 0.001  # Assume 0.1% trading cost
        if trade_value + trade_cost > self.capital:
            # Insufficient capital, cannot execute the trade
            return

        # Update portfolio and capital
        self.positions.append(
            {'price': trade_price, 'quantity': quantity, 'side': side})
        self.capital -= trade_value + trade_cost

    def calculate_portfolio_value(self, current_price):
        # Calculate the current value of the portfolio including positions and capital
        position_values = sum(
            position['price'] * position['quantity'] for position in self.positions)
        return position_values + self.capital


# Historical market data in the form of a list of dictionaries
market_data = market_data_provider.get_market_data(SYMBOL)
trading_algorithm = MovingAverageCrossover()
risk_manager = RiskManager(max_position_size=1000, stop_loss_percentage=5)
starting_capital = 10000


backtester = Backtester(market_data, trading_algorithm,
                        risk_manager, starting_capital)
backtester.run_backtest()

# Calculate portfolio value at the end of the backtest
end_price = market_data[-1]['price']
portfolio_value = backtester.calculate_portfolio_value(end_price)
print(f"Portfolio value at the end of the backtest: {portfolio_value}")
