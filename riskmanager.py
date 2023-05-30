class RiskManager:
    def __init__(self, max_position_size, stop_loss_percentage):
        self.max_position_size = max_position_size
        self.stop_loss_percentage = stop_loss_percentage

    def apply_stop_loss(self, market_data, position_size):
        stop_loss_price = market_data['price'] * \
            (1 - self.stop_loss_percentage / 100)
        if position_size > 0 and market_data['price'] <= stop_loss_price:
            position_size = 0  # Close the position due to stop-loss trigger
        return position_size


risk_manager = RiskManager(max_position_size=1000, stop_loss_percentage=5)
position_size = 500
market_data = {'price': 100}

position_size = risk_manager.apply_stop_loss(market_data, position_size)
if position_size == 0:
    print("Position closed due to stop-loss trigger.")
