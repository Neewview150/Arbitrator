import backtrader as bt
import pandas as pd
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

def run_backtest():
    # Fetch historical data
    data = fetch_historical_data()
    if data is None:
        logging.error("No data fetched for backtesting.")
        return

    # Convert the data to a format compatible with Backtrader
    data_feed = bt.feeds.PandasData(dataname=data)

    # Initialize the Cerebro engine
    cerebro = bt.Cerebro()

    # Add the strategy
    cerebro.addstrategy(SimpleMovingAverageStrategy)

    # Add the data feed
    cerebro.adddata(data_feed)

    # Set initial cash
    cerebro.broker.setcash(10000.0)

    # Run the backtest
    logging.info("Starting backtest...")
    cerebro.run()
    logging.info("Backtest completed.")

    # Plot the results
    cerebro.plot()

if __name__ == '__main__':
    run_backtest()
