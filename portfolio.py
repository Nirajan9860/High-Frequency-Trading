class Portfolio:
    def __init__(self, starting_capital):
        self.starting_capital = starting_capital
        self.capital = starting_capital
        self.positions = []

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


portfolio = Portfolio(starting_capital=10000)
portfolio.add_position('AAPL', 10, 150.25)
portfolio.add_position('GOOG', 5, 2650.75)
portfolio.add_position('MSFT', 8, 350.50)

market_data = [
    {'symbol': 'AAPL', 'price': 155.20},
    {'symbol': 'GOOG', 'price': 2700.80},
    {'symbol': 'MSFT', 'price': 355.00},
    # Add more market data dictionaries as needed
]

portfolio_value = portfolio.calculate_portfolio_value(market_data)
print(f"Portfolio Value: {portfolio_value}")
