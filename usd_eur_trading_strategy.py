import logging
from typing import Dict
import backtrader as bt
import pandas as pd
import requests
from data_fetcher import fetch_historical_data
from datetime import datetime
from colorama import Fore, Style

# Configure logging
logging.basicConfig(filename='trade_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s', filemode='w')

# Constants
LEVERAGE = 100
TRADE_AMOUNT = 2  # Base trade amount in USD
MAX_LEVERAGE_TRADE = TRADE_AMOUNT * LEVERAGE

def fetch_real_time_price():
    """Fetch real-time price for the USD/EUR pair."""
    try:
        api_url = "https://api.exchangerate.host/latest"
        params = {"base": "USD", "symbols": "EUR"}
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        price = data["rates"]["EUR"]
        logging.info(f"Fetched real-time price: {price}")
        return price
    except Exception as e:
        logging.error(f"Error fetching real-time price: {e}")
        return None
    """Calculate the leveraged amount."""
    return amount * LEVERAGE

def risk_management(trade_amount: float, balance: float) -> bool:
    """Ensure the trade does not exceed a certain percentage of the balance."""
    risk_threshold = 0.02  # Risk 2% of the balance
    return trade_amount <= balance * risk_threshold

def execute_trade(trade_amount: float, leverage: bool = False) -> Dict[str, float]:
    """Execute a trade with or without leverage."""
    if leverage:
        trade_amount = calculate_leverage(trade_amount)
    price = fetch_real_time_price()
    if price is None:
        logging.error("Failed to fetch real-time price. Trade aborted.")
        return {"amount": 0, "profit": 0}
    logging.info(f"Executing trade: Amount = ${trade_amount}, Leverage = {leverage}, Price = {price}")
    # Simulate a 1% profit
    return {"amount": trade_amount, "profit": trade_amount * 0.01}

def trade_loop(simulate: bool = True):
    """Continuously execute or simulate trades until stopped by the user."""
    balance = 1000  # Starting balance in USD
    open_orders = 0
    while True:
        if open_orders < 5 and risk_management(TRADE_AMOUNT, balance):
            if simulate:
                result = simulate_trade(TRADE_AMOUNT, leverage=True)
            else:
                result = execute_trade(TRADE_AMOUNT, leverage=True)
            balance += result["profit"]
            open_orders += 1
            logging.info(f"Trade result: {result}, New balance: ${balance}")
            print(Fore.GREEN + f"Trade executed: {result}, New balance: ${balance}" + Style.RESET_ALL)
        else:
            logging.warning("Trade exceeds risk management limits or max open orders reached.")
        
        print("Press Enter to stop or wait for the next trade...")
        try:
            time.sleep(5)  # Wait for 5 seconds before the next trade
        except KeyboardInterrupt:
            break

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
        trade_loop(simulate=True)
    elif mode == 'e':
        trade_loop(simulate=False)
    else:
        logging.warning("Invalid mode selected.")
