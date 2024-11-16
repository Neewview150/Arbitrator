import logging
import time
from typing import Dict
import backtrader as bt
from data_fetcher import fetch_historical_data

# Configure logging
logging.basicConfig(filename='trade_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants
LEVERAGE = 100
TRADE_AMOUNT = 2  # Base trade amount in USD
MAX_LEVERAGE_TRADE = TRADE_AMOUNT * LEVERAGE

def calculate_leverage(amount: float) -> float:
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
    # Simulate trade execution
    logging.info(f"Executing trade: Amount = ${trade_amount}, Leverage = {leverage}")
    # Here you would integrate with FBS API to execute the trade
    return {"amount": trade_amount, "profit": trade_amount * 0.01}  # Simulate a 1% profit

def simulate_trade(trade_amount: float, leverage: bool = False) -> Dict[str, float]:
    """Simulate a trade with or without leverage."""
    if leverage:
        trade_amount = calculate_leverage(trade_amount)
    logging.info(f"Simulating trade: Amount = ${trade_amount}, Leverage = {leverage}")
    return {"amount": trade_amount, "profit": trade_amount * 0.01}  # Simulate a 1% profit

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
    data = fetch_historical_data()
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

def trade_loop(simulate: bool = True):
    """Continuously execute or simulate trades until stopped by the user."""
    balance = 1000  # Starting balance in USD
    while True:
        if risk_management(TRADE_AMOUNT, balance):
            if simulate:
                result = simulate_trade(TRADE_AMOUNT, leverage=True)
            else:
                result = execute_trade(TRADE_AMOUNT, leverage=True)
            balance += result["profit"]
            logging.info(f"Trade result: {result}, New balance: ${balance}")
        else:
            logging.warning("Trade exceeds risk management limits.")
        
        print("Press Enter to stop or wait for the next trade...")
        try:
            time.sleep(5)  # Wait for 5 seconds before the next trade
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    mode = input("Enter 's' to simulate trades, 'e' to execute trades, or 'b' for backtesting: ").strip().lower()
    if mode == 'b':
        run_backtest()
    else:
        simulate_mode = (mode == 's')
        trade_loop(simulate=simulate_mode)
