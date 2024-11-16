import time
import requests
import logging
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO)

# CoinGecko API endpoint
coingecko_api = "https://api.coingecko.com/api/v3"


# Poloniex API endpoint
POLONIEX_API_URL = "https://poloniex.com/public?command=returnTicker"

# List of exchanges to use
exchanges = ["lbank", "kraken", "poloniex", "uniswap"]

def load_symbol_mapping(filename):
    """Load symbol to CoinGecko ID mapping from a text file."""
    symbol_to_id = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():  # Check for non-empty line
                    symbol, coingecko_id = line.strip().split(',')
                    symbol_to_id[symbol] = coingecko_id
        logging.info(f"Loaded symbol mapping: {symbol_to_id}")  # Log the loaded dictionary
    except FileNotFoundError:
        logging.error(f"File {filename} not found.")
    except ValueError:
        logging.error(f"Error processing line in {filename}: Ensure each line is formatted as 'symbol,coingecko_id'.")
    except Exception as e:
        logging.error(f"Error loading symbol mapping: {e}")

    logging.info(f"Type of symbol_to_id: {type(symbol_to_id).__name__}")
    return symbol_to_id  # Ensure this returns a dictionary

def get_mapped_symbols(symbol_to_id):
    """Get all mapped symbols from the CoinGecko ID mapping."""
    if isinstance(symbol_to_id, dict):  # Check if symbol_to_id is a dictionary
        return set(symbol_to_id.keys())
    else:
        logging.error(f"Expected symbol_to_id to be a dictionary, but got {type(symbol_to_id).__name__}.")
        return set()  # Return an empty set if not a dictionary

def fetch_all_mapped_symbols(symbol_to_id):
    """Fetch all mapped symbols from Poloniex."""
    return fetch_symbols('poloniex', symbol_to_id)  # Fetch symbols only from Poloniex

def fetch_symbols(exchange, symbol_to_id):
    """Fetch only the symbols available on Poloniex that match the mapping."""
    try:
        response = requests.get(POLONIEX_API_URL)
        response.raise_for_status()
        data = response.json()

        # Initialize symbols variable
        symbols = {pair.split('_')[0] for pair in data.keys()}
        logging.info(f"Total symbols fetched from Poloniex: {len(symbols)}")

        matched_symbols = symbols.intersection(get_mapped_symbols(symbol_to_id))
        logging.info(f"Fetched and matched symbols from Poloniex: {matched_symbols}")
        return matched_symbols
    except requests.RequestException as e:
        logging.error(f"Error fetching symbols from Poloniex: {e}")
        return set()


def fetch_market_data() -> Dict[str, Dict[str, float]]:
    """Fetch market data from Poloniex."""
    try:
        response = requests.get(POLONIEX_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching market data: {e}")
        return {}

def fetch_and_return_data(symbol_to_id):
    """Fetch prices for all mapped symbols and return them."""
    fetched_symbols = fetch_all_mapped_symbols(symbol_to_id)
    logging.info(f"Fetched and matched symbols: {fetched_symbols}")
    
    # Initialize prices dictionary structured as {symbol: {exchange: price}}
    prices = {symbol: {} for symbol in fetched_symbols}

    # Fetch prices for each symbol from the exchanges
    for symbol in fetched_symbols:
        for exchange in exchanges:
            # Simulate fetching price for the symbol from the exchange
            prices[symbol][exchange] = fetch_price_from_exchange(symbol, exchange)

    return fetched_symbols, prices  # Return both symbols and prices

def fetch_price_from_exchange(symbol, exchange):
    """Simulate fetching price for a symbol from an exchange."""
    # Placeholder function to simulate price fetching
    # In a real scenario, this would involve API calls to the exchange
    return 100.0  # Return a dummy price for simulation purposes
def main():
    """Fetch prices for all mapped symbols and return them."""
    symbol_to_id = load_symbol_mapping("symbols.txt")  # This should be a dictionary
    logging.info(f"Loaded symbol_to_id: {symbol_to_id} (Type: {type(symbol_to_id).__name__})")
    if not isinstance(symbol_to_id, dict) or not symbol_to_id:  # Check if it's a dictionary and not empty
        logging.error("No valid symbol mapping loaded. Exiting.")
        return  # Exit if no mappings were loaded
    prices = fetch_and_return_data(symbol_to_id)
    logging.info(f"Fetched prices: {prices}")

if __name__ == "__main__":
    # Load the symbol mapping first
    symbol_to_id = load_symbol_mapping("symbols.txt")
    
    # Log the loaded mapping for debugging
    logging.info(f"Loaded symbol_to_id: {symbol_to_id} (Type: {type(symbol_to_id).__name__})")

    # Check if symbol_to_id is a dictionary and not empty
    if not isinstance(symbol_to_id, dict) or not symbol_to_id:
        logging.error("No valid symbol mapping loaded. Exiting.")
        exit(1)  # Exit if no mappings were loaded

    # Now fetch the symbols and prices
    symbols, prices = fetch_and_return_data(symbol_to_id)  # Ensure this function returns the correct values
    
    # Proceed to find arbitrage opportunities
    direct_arbitrage_opportunities = find_direct_arbitrage_opportunities(symbols, symbol_to_id, prices)
    triangular_arbitrage_opportunities = find_triangular_arbitrage_opportunities(symbols, symbol_to_id, prices)
    
    # Write the successful arbitrages to a file
    write_successful_arbitrages_to_file(direct_arbitrage_opportunities + triangular_arbitrage_opportunities)
