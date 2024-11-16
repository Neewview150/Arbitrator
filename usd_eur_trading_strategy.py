import logging
from typing import Dict
import backtrader as bt
import pandas as pd
import requests
from data_fetcher import fetch_historical_data

# Configure logging
logging.basicConfig(filename='trade_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants
LEVERAGE = 100
TRADE_AMOUNT = 2  # Base trade amount in USD
MAX_LEVERAGE_TRADE = TRADE_AMOUNT * LEVERAGE

def fetch_historical_data():
    """Fetch historical data for the USD/EUR pair for the past two months."""
    try:
        # Define the API endpoint and parameters
        api_url = "https://api.exchangerate.host/timeseries"
        params = {
            "base": "USD",
            "symbols": "EUR",
            "start_date": "2023-08-01",
            "end_date": "2023-10-01"
        }
        
        # Make the API request
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        # Parse the response JSON and convert it to a DataFrame
        data = response.json()
        rates = data.get("rates", {})
        df = pd.DataFrame.from_dict(rates, orient='index')
        df.index = pd.to_datetime(df.index)
        df.columns = ["close"]
        
        logging.info(f"Fetched historical data: {df.head()}")
        return df
    except Exception as e:
        logging.error(f"Error fetching historical data: {e}")
        return None
    """Calculate the leveraged amount."""
    return amount * LEVERAGE

def risk_management(trade_amount: float, balance: float) -> bool:
    """Ensure the trade does not exceed a certain percentage of the balance."""
    risk_threshold = 0.02  # Risk 2% of the balance
    return trade_amount <= balance * risk_threshold

def simulate_trade(trade_amount: float, leverage: bool = False) -> Dict[str, float]:
    """Simulate a trade with or without leverage."""
    if leverage:
        trade_amount = calculate_leverage(trade_amount)
    logging.info(f"Simulating trade: Amount = ${trade_amount}, Leverage = {leverage}")
    return {"amount": trade_amount, "profit": trade_amount * 0.01}  # Simulate a 1% profit

def simulate_trades_with_historical_data():
    """Simulate trades using historical data."""
    data = fetch_historical_data()  # Use the newly defined function
    if data is None:
        logging.error("No historical data available for simulation.")
        return

    balance = 1000  # Starting balance in USD
    for index, row in data.iterrows():
        if risk_management(TRADE_AMOUNT, balance):
            result = simulate_trade(TRADE_AMOUNT, leverage=True)
            balance += result["profit"]
            logging.info(f"Simulated trade result: {result}, New balance: ${balance}")
        else:
            logging.warning("Trade exceeds risk management limits.")

class SimpleMovingAverageStrategy(bt.Strategy):
    params = (
        ('sma_period', 15),
    )

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.buy(size=100)
                logging.info(f"Buying at {self.data.close[0]}")
        else:
            if self.data.close[0] < self.sma[0]:
                self.sell(size=100)
                logging.info(f"Selling at {self.data.close[0]}")

def run_backtest():
    data = fetch_historical_data()  # Use the newly defined function
    if data is None:
        logging.error("No data fetched for backtesting.")
        return

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SimpleMovingAverageStrategy)
    cerebro.adddata(data_feed)
    cerebro.broker.setcash(10000.0)

    logging.info("Starting backtest...")
    cerebro.run()
    logging.info("Backtest completed.")
    cerebro.plot()

def simulate_trades_with_historical_data():
    """Simulate trades using historical data."""
    data = fetch_historical_data()  # Use the newly defined function
    if data is None:
        logging.error("No historical data available for simulation.")
        return

    balance = 1000  # Starting balance in USD
    for index, row in data.iterrows():
        if risk_management(TRADE_AMOUNT, balance):
            result = simulate_trade(TRADE_AMOUNT, leverage=True)
            balance += result["profit"]
            logging.info(f"Simulated trade result: {result}, New balance: ${balance}")
        else:
            logging.warning("Trade exceeds risk management limits.")

if __name__ == "__main__":
    mode = input("Enter 's' to simulate trades, 'e' to execute trades, or 'b' for backtesting: ").strip().lower()
    if mode == 'b':
        run_backtest()
    elif mode == 's':
        simulate_trades_with_historical_data()
    else:
        logging.warning("Live execution mode is not supported in this simulation-focused version.")
