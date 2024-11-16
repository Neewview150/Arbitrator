import logging
import requests
import json
from typing import List, Dict
from data_fetcher import fetch_and_return_data
from web3 import Web3
from web3.middleware import geth_poa_middleware

def find_direct_arbitrage_opportunities(symbols, symbol_to_id, prices, fee_percentage=0.002):
    """Find direct arbitrage opportunities between exchanges."""
    arbitrage_opportunities = []
    for symbol in symbols:
        for exchange1 in exchanges:
            for exchange2 in exchanges:
                if exchange1 != exchange2:
                    price1 = prices[symbol][exchange1]
                    price2 = prices[symbol][exchange2]
                    if price1 > price2:
                        profit = simulate_trade(symbol, symbol, symbol, exchange1, exchange2, exchange2, price1, price2, price2, fee_percentage)
                        if profit > 0:
                            arbitrage_opportunities.append((symbol, exchange1, exchange2, price1, price2, profit))
    return arbitrage_opportunities
def find_triangular_arbitrage_opportunities(symbols, symbol_to_id, prices, fee_percentage=0.002):
    """Find triangular arbitrage opportunities between exchanges, ensuring all symbols are distinct."""
    triangular_arbitrage_opportunities = []
    
    for symbol1 in symbols:
        for symbol2 in symbols:
            for symbol3 in symbols:
                # Ensure all symbols are distinct
                if symbol1 != symbol2 and symbol2 != symbol3 and symbol1 != symbol3:
                    for exchange1 in exchanges:
                        for exchange2 in exchanges:
                            for exchange3 in exchanges:
                                # Ensure all exchanges are distinct
                                if exchange1 != exchange2 and exchange2 != exchange3 and exchange1 != exchange3:
                                    price1 = prices[symbol1][exchange1]
                                    price2 = prices[symbol2][exchange2]
                                    price3 = prices[symbol3][exchange3]

                                    if price1 > 0 and price2 > 0 and price3 > 0:
                                        profit = simulate_trade(symbol1, symbol2, symbol3, exchange1, exchange2, exchange3, price1, price2, price3, fee_percentage)
                                        
                                        # Check if the profit is positive
                                        if profit > 0:
                                            triangular_arbitrage_opportunities.append(
                                                (symbol1, symbol2, symbol3, exchange1, exchange2, exchange3, price1, price2, price3, profit)
                                            )
    return triangular_arbitrage_opportunities

def simulate_trade(symbol1, symbol2, symbol3, exchange1, exchange2, exchange3, price1, price2, price3, fee_percentage):
    """Simulate a triangular trade and return the profit amount."""
    # Assume starting with 1 unit of symbol2
    investment = 1.0  # Starting with 1 unit of symbol2

    # Step 1: Buy symbol1 using symbol2 on exchange2
    amount_symbol1 = investment / price2  # Amount of symbol1 we can buy
    cost_symbol1 = amount_symbol1 * price2 * (1 + fee_percentage)  # Cost including fee on exchange2

    # Step 2: Buy symbol 3 using symbol1 on exchange1
    amount_symbol3 = amount_symbol1 * price1  # Amount of symbol3 we can buy
    cost_symbol3 = amount_symbol3 * price1 * (1 + fee_percentage)  # Cost including fee on exchange1

    # Step 3: Sell symbol3 for symbol2 on exchange3
    final_amount_symbol2 = amount_symbol3 * (price3 * (1 - fee_percentage))  # Amount of symbol2 after selling

    # Calculate profit
    profit = final_amount_symbol2 - investment  # Profit from the trade

    return profit  # Return the profit amount

def identify_arbitrage_opportunities(market_data: Dict[str, Dict[str, float]]) -> List[Dict[str, str]]:
    """Identify triangular arbitrage opportunities."""
    opportunities = []
    pairs = list(market_data.keys())

    for i, pair1 in enumerate(pairs):
        for j, pair2 in enumerate(pairs):
            if i == j:
                continue
            for k, pair3 in enumerate(pairs):
                if k == i or k == j:
                    continue

                if pair1.split('_')[1] == pair2.split('_')[0] and pair2.split('_')[1] == pair3.split('_')[0] and pair3.split('_')[1] == pair1.split('_')[0]:
                    rate1 = market_data[pair1]['last']
                    rate2 = market_data[pair2]['last']
                    rate3 = market_data[pair3]['last']

                    profit = (1 / rate1) * rate2 * rate3 - 1
                    if profit > 0:
                        opportunities.append({
                            "pair1": pair1,
                            "pair2": pair2,
                            "pair3": pair3,
                            "profit": profit
                        })
    return opportunities

def scan_arbitrage_opportunities(api_key: str, api_secret: str) -> List[Dict[str, str]]:
    """Scan for arbitrage opportunities."""
    market_data = fetch_market_data(api_key, api_secret)
    if not market_data:
        return []

    opportunities = identify_arbitrage_opportunities(market_data)
    return opportunities

def load_abi(file_path):
    """Load ABI from a JSON file."""
    with open(file_path, 'r') as abi_file:
        return json.load(abi_file)

def execute_trade(opportunity, contract_address, provider_url):
    """Execute trade using flash loans."""
    try:
        # Load the ABI
        abi = load_abi('abi.json')

        # Connect to the blockchain
        web3 = Web3(Web3.HTTPProvider(provider_url))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not web3.isConnected():
            logging.error("Failed to connect to the blockchain")
            return

        # Load the flash loan contract
        contract = web3.eth.contract(address=contract_address, abi=abi)

        # Prepare transaction parameters
        account = web3.eth.account.from_key('YOUR_PRIVATE_KEY')  # Replace with secure key management
        nonce = web3.eth.getTransactionCount(account.address)
        gas_price = web3.eth.gas_price

        # Define the transaction
        transaction = contract.functions.executeFlashLoan(
            web3.toWei(1, 'ether'),  # Example amount, replace with actual logic
            [opportunity['pair1'], opportunity['pair2'], opportunity['pair3']]
        ).buildTransaction({
            'chainId': 1,  # Mainnet chain ID, replace if using a testnet
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': nonce
        })

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key='YOUR_PRIVATE_KEY')  # Replace with secure key management

        # Send the transaction
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        logging.info(f"Transaction sent with hash: {web3.toHex(tx_hash)}")

        # Wait for the transaction receipt
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logging.info(f"Transaction receipt: {receipt}")

    except Exception as e:
        logging.error(f"Error executing arbitrage: {e}")

def prompt_user_for_trade(opportunity):
    """Prompt user to confirm trade execution."""
    print(f"Opportunity found: {opportunity}")
    choice = input("Do you want to execute this trade? (yes/no): ")
    return choice.lower() == 'yes'

def write_successful_arbitrages_to_file(opportunities):
    """Write successful arbitrage opportunities to a text file."""
    with open("arbitrage_opportunities.txt", "w") as file:
        for opportunity in opportunities:
            file.write(f"{opportunity}\n")

def execute_arbitrage(opportunity, contract_address, provider_url):
    """Execute arbitrage using a flash loan."""
    try:
        # Load the ABI
        abi = load_abi('abi.json')

        # Connect to the blockchain
        web3 = Web3(Web3.HTTPProvider(provider_url))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not web3.isConnected():
            logging.error("Failed to connect to the blockchain")
            return

        # Load the flash loan contract
        contract = web3.eth.contract(address=contract_address, abi=abi)

        # Prepare transaction parameters
        account = web3.eth.account.from_key('YOUR_PRIVATE_KEY')  # Replace with secure key management
        nonce = web3.eth.getTransactionCount(account.address)
        gas_price = web3.eth.gas_price

        # Define the transaction
        transaction = contract.functions.executeFlashLoan(
            web3.toWei(1, 'ether'),  # Example amount, replace with actual logic
            [opportunity['pair1'], opportunity['pair2'], opportunity['pair3']]
        ).buildTransaction({
            'chainId': 1,  # Mainnet chain ID, replace if using a testnet
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': nonce
        })

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key='YOUR_PRIVATE_KEY')  # Replace with secure key management

        # Send the transaction
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        logging.info(f"Transaction sent with hash: {web3.toHex(tx_hash)}")

        # Wait for the transaction receipt
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logging.info(f"Transaction receipt: {receipt}")

    except Exception as e:
        logging.error(f"Error executing arbitrage: {e}")

if __name__ == "__main__":
    symbols, prices, symbol_to_id = fetch_and_return_data("symbols.txt")
    direct_arbitrage_opportunities = find_direct_arbitrage_opportunities(symbols, symbol_to_id, prices)
    triangular_arbitrage_opportunities = find_triangular_arbitrage_opportunities(symbols, symbol_to_id, prices)
    for opportunity in triangular_arbitrage_opportunities:
        if prompt_user_for_trade(opportunity):
            execute_trade(opportunity, 'CONTRACT_ADDRESS', 'PROVIDER_URL')  # Replace with actual contract address and provider URL

    write_successful_arbitrages_to_file(direct_arbitrage_opportunities + triangular_arbitrage_opportunities)
