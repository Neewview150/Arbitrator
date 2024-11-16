# Arbitrator

## Introduction

Arbitrator is a tool designed to identify and exploit arbitrage opportunities in cryptocurrency markets. It fetches real-time price data from multiple exchanges and analyzes it to find both direct and triangular arbitrage opportunities. The project includes a web interface to visualize trading data and arbitrage opportunities using dynamic charts.

## Installation

To set up the project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Neewview150/Arbitrator.git
   cd Arbitrator
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Backtesting

To backtest a trading strategy using historical data, follow these steps:

### Prerequisites

- Ensure you have set up the environment and installed all dependencies as described in the Installation section.

### Running the Backtest

1. **Fetch Historical Data**:
   The backtest uses historical data for the USD/EUR pair. Ensure you have internet access to fetch this data.

2. **Execute the Backtest Script**:
   Run the following command to start the backtest:

   ```bash
   python backtest_strategy.py
   ```

   This script will execute a simple moving average strategy on the fetched data.

### Interpreting Results

- **Logs**: The script logs buy and sell actions with the corresponding prices.
- **Plot**: After the backtest completes, a plot will be displayed showing the price data and the moving average.

## Usage

## Backtesting the USD/EUR Trading Strategy

This section provides instructions on how to backtest the USD/EUR trading strategy using historical data.

### Prerequisites

- Ensure you have set up the environment and installed all dependencies as described in the Installation section.

### Running the Backtest

1. **Fetch Historical Data**:
   The backtest uses historical data for the USD/EUR pair. Ensure you have internet access to fetch this data.

2. **Execute the Backtest Script**:
   Run the following command to start the backtest:

   ```bash
   python usd_eur_trading_strategy.py
   ```

   You will be prompted to choose between simulating trades, executing trades, or running a backtest. Enter 'b' for backtesting.

### Interpreting Results

- **Logs**: The script logs buy and sell actions with the corresponding prices.
- **Plot**: After the backtest completes, a plot will be displayed showing the price data and the moving average.

## USD/EUR Trading Strategy

This section describes a trading strategy for the USD/EUR currency pair using leverage. The strategy aims to exploit short-term price movements with a focus on risk management and ethical trading practices.

### Purpose

The strategy is designed to be frequently profitable by leveraging trades on the USD/EUR pair. It incorporates risk management techniques to ensure that trades do not exceed a certain percentage of the account balance.

### Implementation

The strategy is implemented in Python and uses a leverage of 100%. It includes functions for calculating leverage, managing risk, and executing or simulating trades. Trades are logged for analysis and review.

### Prerequisites

- Python 3.x
- Required Python packages listed in `requirements.txt`
- Access to the FBS trading platform API (or simulation mode)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Neewview150/Arbitrator.git
   cd Arbitrator
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Strategy

To run the USD/EUR trading strategy, execute the following command:

```bash
python usd_eur_trading_strategy.py
```

You will be prompted to choose between simulating trades or executing them. Enter 's' for simulation or 'e' for execution.

### Interpreting Results

- **Trade Logs**: All trades are logged in `trade_log.txt` with details of each trade, including the amount, leverage, and profit.
- **Balance Updates**: The script outputs the new balance after each trade, allowing you to track performance over time.

## Usage

To run the project and start the web interface, execute the following command:

```bash
python app.py
```

This will start a local server. Open your web browser and navigate to `http://localhost:5000` to access the interface. Here, you can view charts of trading data and a list of current arbitrage opportunities.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear and descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
