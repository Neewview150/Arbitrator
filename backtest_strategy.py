import backtrader as bt
import logging
from data_fetcher import fetch_historical_data

# Configure logging
logging.basicConfig(level=logging.INFO)

class SimpleMovingAverageStrategy(bt.Strategy):
    params = (
        ('sma_period', 15),
    )

    def __init__(self):
        # Initialize the simple moving average indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.sma_period
        )

    def next(self):
        # Check if we are in the market
        if not self.position:
            # If not in the market, check if we should buy
            if self.data.close[0] > self.sma[0]:
                self.buy(size=100)  # Example buy size
                logging.info(f"Buying at {self.data.close[0]}")
        else:
            # If in the market, check if we should sell
            if self.data.close[0] < self.sma[0]:
                self.sell(size=100)  # Example sell size
                logging.info(f"Selling at {self.data.close[0]}")

def simulate_trades_with_historical_data():
    """Simulate trades using historical data."""
    data = fetch_historical_data()
    if data is None:
        logging.error("No historical data available for simulation.")
        return

    balance = 1000  # Starting balance in USD
    for index, row in data.iterrows():
        if row['Close'] > row['Open']:  # Example condition for buying
            logging.info(f"Simulating buy at {row['Close']} on {index}")
            balance += 10  # Simulate profit
        elif row['Close'] < row['Open']:  # Example condition for selling
            logging.info(f"Simulating sell at {row['Close']} on {index}")
            balance -= 10  # Simulate loss

    logging.info(f"Final balance after simulation: ${balance}")

if __name__ == '__main__':
    simulate_trades_with_historical_data()
